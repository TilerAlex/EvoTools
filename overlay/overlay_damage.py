import tkinter as tk
from utils import utils
from win32 import win32gui
import win32con
import os
from dataclasses import dataclass, field
from typing import List
import time

POS_TOP_RIGHT = 'Top Right'
POS_BOT_RIGHT = 'Bot Right'

overlay_positions = [
    POS_TOP_RIGHT,
    POS_BOT_RIGHT,
]

overlay_visible = False
prev_menu = None
prev_menu_text = None
prev_width = 0
prev_height = 0
prev_x = 0
prev_y = 0
prev_file_update = None
_file_path = None
_file_record = None

player_color = {
    0: 'red4',
    1: 'blue2',
    2: 'cyan4',
    3: 'purple4',
    4: 'yellow4',
    5: 'orange3',
    6: 'green',
    7: 'pink3',
    8: 'grey40',
    9: 'skyblue4'
}

_enabled = False
_current_position = POS_BOT_RIGHT
_prev_position = None

def toggle_damage_overlay():
    global _enabled
    _enabled = not _enabled

def get_overlay_position():
    return _current_position

def set_overlay_position():
    global _current_position
    index = overlay_positions.index(_current_position)
    index = (index + 1) % len(overlay_positions)
    _current_position = overlay_positions[index]


@dataclass
class ObjectInfo:
    name: str = None       # Column name
    value: int = None      # Damage %

@dataclass
class ObjectRecord:
    name: str = None
    values: List[int] = field(default_factory=list)

@dataclass
class PlayerRecord:
    index: int = None
    color: str = None
    nick: str = None
    hero: str = None
    objects: List[ObjectInfo] = field(default_factory=list)

@dataclass
class FileRecord:
    map: str = None
    index_arr: List[int] = field(default_factory=list)
    color_arr: List[str] = field(default_factory=list)
    nick_arr: List[str] = field(default_factory=list)
    hero_arr: List[str] = field(default_factory=list)
    object_arr: List[ObjectRecord] = field(default_factory=list)


def is_game_resolution_changed():
    global prev_width, prev_height
    # Resolution or window size (windowed)
    if prev_width != utils._width or prev_height != utils._height:
        prev_width = utils._width
        prev_height = utils._height
        return True
    return False

def is_game_position_changed():
    global prev_x, prev_y
    if prev_x != utils._x or prev_y != utils._y:
        # Position when windowed
        prev_x = utils._x
        prev_y = utils._y
        return True
    return False

def is_overlay_position_changed():
    global _prev_position
    if _prev_position != _current_position:
        _prev_position = _current_position
        return True
    return False

def get_overlay_offset(width, height):
    if _current_position == POS_TOP_RIGHT:
        offset_x = utils._width - width
        offset_y = int(utils._height / 24)
    elif _current_position == POS_BOT_RIGHT:
        offset_x = utils._width - width
        offset_y = int(utils._height / 1.37) - height
    return offset_x, offset_y

def adjust_overlay_position(root: tk.Tk):
    # Get current overlay size
    width = root.winfo_width()
    height = root.winfo_height()
    offset_x, offset_y = get_overlay_offset(width, height)
    x = utils._x + offset_x
    y = utils._y + offset_y
    root.geometry(f"{width}x{height}+{x}+{y}")

def adjust_overlay_size(root: tk.Tk):
    # Changes overlay size to fit all widgets
    width = root.winfo_reqwidth()
    height = root.winfo_reqheight()
    offset_x, offset_y = get_overlay_offset(width, height)
    x = utils._x + offset_x
    y = utils._y + offset_y
    root.geometry(f"{width}x{height}+{x}+{y}")

def hide_overlay(root: tk.Tk):
    if root.winfo_width() > 1:
        root.geometry(f"{0}x{0}")

# def is_damage_file_exists(path: str):
#     return os.path.isfile(path + 'Damage.txt')

def get_line_value(str: str):
    start = str.find('"')+1
    end = str.rfind('"')
    return str[start:end]

def get_player_data(str: str) -> PlayerRecord:
    line = get_line_value(str)
    record = PlayerRecord()

    parts = line.split(" - ")

    full_nick = parts[0].strip()
    record.nick = full_nick.split("#")[0]
    record.hero = parts[1].strip()

    objects_string = parts[2].strip()

    for obj in objects_string.split("//"):
        name, value = obj.split(":")

        object = ObjectInfo()
        object.name = name.strip()
        object.value = int(value.strip())

        record.objects.append(object)

    return record


def get_file_path() -> str:
    map_path = utils._map_root_path
    if map_path != None:
        file_path = map_path + 'Damage.txt'
        if os.path.isfile(file_path):
            return file_path
    return None

def is_file_modified():
    global prev_file_update

    # If file exists
    if _file_path != None:
        timestamp = os.path.getmtime(_file_path)
        if prev_file_update != timestamp:
            prev_file_update = timestamp
            return True
    return False

def read_file(file_path: str) -> FileRecord:

    file_record = FileRecord()

    # Read file
    line_arr = []
    with open(file_path, "r", encoding="utf-8") as file:
        line_arr = file.readlines()

    # Skip processing
    if len(line_arr) < 16:
        return None

    file_record.map = get_line_value(line_arr[3])

    # Parse player records (10 lines)
    player_record_arr: List[PlayerRecord] = []
    for i in range(5, 15):
        player_record = get_player_data(line_arr[i])                # lines [5-14]
        player_record.index = i-5                                   # player index [0-9]
        player_record.color = player_color[player_record.index]     # colors [0-9]
        # Skip inactive/computer players
        if player_record.hero != '':
            player_record_arr.append(player_record)

    # Sort by damage
    player_record_arr = sorted(
        player_record_arr,
        key = lambda player_record: sum(obj.value for obj in player_record.objects if obj.value is not None),
        reverse = True
    )

    # Transform "line data type" structure to "column data type" structure
    for player_record in player_record_arr:
        file_record.index_arr.append(player_record.index)
        file_record.color_arr.append(player_record.color)
        file_record.nick_arr.append(player_record.nick)
        file_record.hero_arr.append(player_record.hero)
        damage_columns = len(player_record.objects)

    # Damage columns
    for j in range(damage_columns):
        object_record = ObjectRecord()
        for player_record in player_record_arr:
            object_record.name = player_record.objects[j].name
            object_record.values.append(player_record.objects[j].value)
        file_record.object_arr.append(object_record)

    return file_record


def draw_canvas(root: tk.Tk, canvas: tk.Canvas, file_record: FileRecord):
    if file_record is None:
        return

    height = utils._height

    # Calculate sizes
    border_size = int(height / (1080 / 10))
    line_height = int(height / (1080 / 20))
    player_nick_width = int(height / (1080 / 110))
    object_bar_width = int(height / (1080 / 70))
    space_between_columns = int(height / (1080 / 10))
    font_size = int(height / (1080 / 10))

    canvas.pack_configure(padx=border_size, pady=border_size)

    x_offset = 0
    y_offset = 0

    x = x_offset
    y = y_offset

    # Map name
    canvas.create_text((x, y), anchor=tk.NW, text=file_record.map, font=("Tahoma", font_size), fill="yellow")
    y += line_height

    # Player nicks
    for player_nick in file_record.nick_arr:
        # canvas.create_text((x, y+2), anchor=tk.NW, text=player_nick, font=("Tahoma", font_size), fill="white")
        canvas.create_text((x+player_nick_width, y+2), anchor=tk.NE, text=player_nick, font=("Tahoma", font_size), fill="white")
        y += line_height

    x += player_nick_width + space_between_columns

    # Damage columns
    for object in file_record.object_arr:

        max_value = max(object.values)

        # Skip empty column
        if max_value == 0:
            continue

        y = y_offset

        # Column name
        canvas.create_text((x, y), anchor=tk.NW, text=object.name[:12], font=("Tahoma", font_size), fill="grey75")
        y += line_height
        x1 = x
        y1 = y

        # Column bars
        for j in range(len(object.values)):
            value = object.values[j]
            color = file_record.color_arr[j]
            length = int(value / max_value * object_bar_width)

            # x1 = x
            x2 = x1 + length
            y2 = y1 + line_height
            if value != 0:
                canvas.create_rectangle(x1, y1, x2, y2, fill=color, width=0)
                canvas.create_text((x1+5, y1+2), anchor=tk.NW, text=f"{value}", font=("Tahoma", font_size), fill="white")
            y1 = y1 + line_height

        x += object_bar_width + space_between_columns

    # Update layout (forces Tkinter to process all "pending idle tasks" immediately)
    canvas.update_idletasks()

    # Get bounding box of ALL items
    bbox = canvas.bbox("all")

    if bbox:
        x1, y1, x2, y2 = bbox
        width = x2 - x1
        height = y2 - y1

        # Resize the Canvas
        canvas.config(width=width, height=height)

    # Update root
    root.update()

def redraw_canvas(root: tk.Tk, canvas: tk.Canvas, file_record: FileRecord):
    canvas.delete("all")
    draw_canvas(root, canvas, file_record)
    adjust_overlay_size(root)

def reload_canvas(root: tk.Tk, canvas: tk.Canvas):
    global _file_record
    _file_record = read_file(_file_path)
    redraw_canvas(root, canvas, _file_record)

def update_overlay(root, canvas):
    global overlay_visible

    # Show/Hide overlay
    if utils.is_warcraft_active() and utils._warcraft_foreground:
        # overlay_visible = _enabled
        if not overlay_visible and _enabled:
            overlay_visible = True
            adjust_overlay_size(root)
        elif overlay_visible and not _enabled:
            overlay_visible = False
            hide_overlay(root)
    else:
        if overlay_visible:
            overlay_visible = False
            hide_overlay(root)

    # Update overlay
    if overlay_visible:
        is_game_res_changed = is_game_resolution_changed()
        is_game_pos_changed = is_game_position_changed()
        is_overlay_pos_changed = is_overlay_position_changed()
        if is_game_res_changed or is_game_pos_changed or is_overlay_pos_changed:
            adjust_overlay_position(root)
        if is_game_res_changed:
            redraw_canvas(root, canvas, _file_record)

        if is_file_modified():
            reload_canvas(root, canvas)

    root.after(100, update_overlay, root, canvas)


def create_overlay():
    root = tk.Tk()
    root.title("Damage meter")
    root.geometry(f"{0}x{0}+{0}+{0}")
    root.attributes("-topmost", True)     # always on top
    root.attributes("-alpha", 0.7)
    root.attributes("-disabled", True)
    # root.attributes("-transparentcolor", 'black')
    root.config(bg='black')
    root.overrideredirect(True)
    root.update()

    hwnd = win32gui.GetParent(root.winfo_id())

    styles = win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE)
    styles = styles | win32con.WS_EX_NOACTIVATE      # does not become the foreground window when the user clicks it
    styles = styles | win32con.WS_EX_APPWINDOW       # Forces a top-level window onto the taskbar when the window is visible
    styles = styles | win32con.WS_EX_LAYERED         # The window is a layered window
    styles = styles | win32con.WS_EX_TRANSPARENT     # ignores mouse over it
    win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE, styles)
    styles_pos = win32con.SWP_NOACTIVATE                   # Does not activate the window
    styles_pos = styles_pos | win32con.SWP_NOSIZE          # Retains the current size
    styles_pos = styles_pos | win32con.SWP_NOMOVE          # Retains the current position
    styles_pos = styles_pos | win32con.SWP_FRAMECHANGED    # Applies new frame styles set using the "SetWindowLong" function
    styles_pos = styles_pos | win32con.SWP_NOZORDER        # Retains the current Z order
    win32gui.SetWindowPos(hwnd, win32con.HWND_NOTOPMOST, 0, 0, 0, 0, styles_pos)

    canvas = tk.Canvas(root, bg='black', highlightthickness=0)
    canvas.pack()

    return root, canvas

def run_overlay():
    global _file_path
    _file_path = get_file_path()

    time.sleep(0.25)     # workaround to avoid "pywintypes.error: (5, 'SetWindowPos', 'Access is denied.')"
    root, canvas = create_overlay()
    root.after(0, update_overlay, root, canvas)
    root.mainloop()
