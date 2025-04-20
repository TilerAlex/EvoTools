import tkinter as tk
from utils import constants, utils
from overlay import controls
from jobs import clues, fishing, leveling
from win32 import win32gui
import main
import win32con

overlay_visible = False
prev_menu = None
prev_menu_text = None
prev_width = 0
prev_height = 0
prev_x = 0
prev_y = 0


def is_resolution_changed():
    global prev_width, prev_height
    # Resolution or window size (windowed)
    if prev_width != utils._width or prev_height != utils._height:
        prev_width = utils._width
        prev_height = utils._height
        return True
    return False

def is_position_changed():
    global prev_x, prev_y
    if prev_x != utils._x or prev_y != utils._y:
        # Position when windowed
        prev_x = utils._x
        prev_y = utils._y
        return True
    return False

def get_overlay_offset():
    # Calculate overlay offset based on game resolution
    offset_x = int(utils._height / 13.5)
    offset_y = int(utils._height / 22)
    return offset_x, offset_y

def adjust_position(root: tk.Tk):
    # Get current overlay size
    width = root.winfo_width()
    height = root.winfo_height()
    offset_x, offset_y = get_overlay_offset()
    x = utils._x + offset_x
    y = utils._y + offset_y
    root.geometry(f"{width}x{height}+{x}+{y}")

def adjust_size(root: tk.Tk):
    # Changes overlay size to fit all widgets
    width = root.winfo_reqwidth()
    height = root.winfo_reqheight()
    offset_x, offset_y = get_overlay_offset()
    x = utils._x + offset_x
    y = utils._y + offset_y
    root.geometry(f"{width}x{height}+{x}+{y}")


def hide_overlay(root: tk.Tk):
    if root.winfo_width() > 1:
        root.geometry(f"{0}x{0}")

# not used
def show_overlay(root: tk.Tk):
    if root.winfo_width() == 1:
        width = root.winfo_reqwidth()
        height = root.winfo_reqheight()
        root.geometry(f"{width}x{height}")

def adjust_label_font(label: tk.Label):
    if is_resolution_changed():
        font_size = int(utils._height / (1080 / 10))
        label.config(font=("Tahoma", font_size))

def update_overlay(root: tk.Tk, label: tk.Label):
    global overlay_visible #, prev_menu, prev_menu_text

    # Show/Hide overlay
    if utils.is_warcraft_active() and utils._warcraft_foreground:
        if not overlay_visible:
            overlay_visible = True
            # root.deiconify()          # show the widget
    else:
        if overlay_visible:
            overlay_visible = False
            # root.withdraw()          # hide the widget

    # Set overlay text
    if overlay_visible:
        # show_overlay(root)

        # If game resolution or window position is changed
        # if is_resolution_changed() or is_position_changed():
        #     adjust_position(root)

        # Menu
        current_menu = controls.get_current_menu()

        error_suffix = ""
        if utils._resolution not in [constants.RES_1080, constants.RES_1440, constants.RES_1600]:
            error_suffix = "(unsupported resolution)"

        label_text = f"{controls.custom_names[current_menu]()} {error_suffix}\n"

        for hotkey, action in controls.controls[current_menu].items():
            if isinstance(action, str):
                prefix = '> '
                if (action == controls.MENU_MAIN and current_menu in (controls.MENU_AUTOMATION, controls.MENU_DAMAGE, controls.MENU_SYSTEM) or
                    action == controls.MENU_AUTOMATION and current_menu in (controls.MENU_CLUE, controls.MENU_ARROWS, controls.MENU_FISHING, controls.MENU_LEVELING)):
                    prefix = '< '
                label_temp = f"{prefix}{controls.custom_names.get(action, lambda: action)()}"
                label_text += f"{hotkey}: {label_temp}\n"
            else:
                action_name = action.__name__
                prefix = ' - '
                label_temp = f"{prefix}{controls.custom_names.get(action_name, lambda: action_name)()}"
                label_text += f"{hotkey}: {label_temp}\n"

        # Additional items (non-interactable)
        if current_menu == controls.MENU_CLUE:
            label_text += f"Last clue: {clues.get_last_pos_str()}\n"
        elif current_menu == controls.MENU_FISHING:
            label_text += f"Score: {fishing.score}/{fishing.get_fishing_mode_params()[fishing.SCORE_LIMIT]} ({fishing.iteration}/20)\n"
            if fishing._enabled and fishing.get_save_interval() != None:
                label_text += f"Auto-save in: {fishing.get_time_to_save()}"
        elif current_menu == controls.MENU_LEVELING:
            if leveling._enabled and leveling.get_save_interval() != None:
                label_text += f"Auto-save in: {leveling.get_time_to_save()}"
        elif current_menu == controls.MENU_SYSTEM:
            label_text += f"Game resolution: {utils._resolution}\n"
            label_text += f"Window offset: {utils._x}x{utils._y}\n"
            label_text += f"Version: {main.VERSION}\n"
        label_text = label_text.rstrip("\n")

        # Set Lable text
        label.config(text=label_text)

        adjust_label_font(label)
        root.update()
        adjust_size(root)
    else:
        hide_overlay(root)

    root.after(100, update_overlay, root, label)

def create_overlay():
    root = tk.Tk()
    root.title("Menu")
    root.geometry(f"{0}x{0}+{0}+{0}")
    root.attributes("-topmost", True)     # always on top
    root.attributes("-alpha", 0.7)
    root.attributes("-disabled", True)
    root.attributes("-transparentcolor", 'black')
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

    label = tk.Label(root, text='', font=('Tahoma', 12), bg='black', fg='white', anchor=tk.NW, justify=tk.LEFT)
    label.pack(fill=tk.BOTH, expand=tk.TRUE)

    return root, label

def run_overlay():
    root, label = create_overlay()
    root.after(0, update_overlay, root, label)
    root.mainloop()
