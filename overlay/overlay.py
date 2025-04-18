from tkinter import Tk, Label
from utils import constants, utils
from overlay import controls
from jobs import clues, fishing, leveling
from win32 import win32gui
import main
import win32con

OVERLAY_WIDTH = 450
OVERLAY_HEIGHT = 300
OVERLAY_X = 100
OVERLAY_Y = 50

overlay_visible = True
prev_menu = None
prev_menu_text = None
prev_width = 0
prev_height = 0
prev_x = 0
prev_y = 0


def update_overlay(root, label):
    global overlay_visible, prev_width, prev_height, prev_x, prev_y, prev_menu, prev_menu_text

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

        # If game resolution or window position is changed
        if prev_width != utils._width or prev_height != utils._height or prev_x != utils._x or prev_y != utils._y:
            prev_width = utils._width
            prev_height = utils._height
            prev_x = utils._x
            prev_y = utils._y
            if utils._height <= 1080:
                root.geometry(f"{OVERLAY_WIDTH}x{OVERLAY_HEIGHT}+{utils._x + 80}+{utils._y + 30}")
            elif utils._height == 1440:
                root.geometry(f"{OVERLAY_WIDTH}x{OVERLAY_HEIGHT}+{utils._x + 110}+{utils._y + 50}")
            elif utils._height >= 1600:
                root.geometry(f"{OVERLAY_WIDTH}x{OVERLAY_HEIGHT}+{utils._x + 120}+{utils._y + 60}")

        current_menu = controls.get_current_menu()

        error_suffix = "(unsupported resolution)" if utils._resolution not in [constants.RES_1080, constants.RES_1440, constants.RES_1600] else ""

        label_text = f"{controls.custom_names[current_menu]()} {error_suffix}\n"
        for hotkey, action in controls.controls[current_menu].items():
            if isinstance(action, str):
                label_text += f"{hotkey}: {controls.custom_names[action]()}\n"
            else:
                action_name = action.__name__
                label_text += f"{hotkey}: {controls.custom_names.get(action_name, lambda: action_name)()}\n"

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

        # Replace overlay lable with new text
        label.config(text=label_text)
    else:
        label.config(text='')

    root.after(100, update_overlay, root, label)

# Create Widget
def create_overlay():
    root = Tk()
    root.title("Overlay")
    root.geometry(f"{OVERLAY_WIDTH}x{OVERLAY_HEIGHT}+{OVERLAY_X}+{OVERLAY_Y}")
    root.attributes("-topmost", True)     # always on top
    root.attributes("-alpha", 0.7)
    root.attributes("-disabled", True)
    root.configure(bg='black')
    root.wm_attributes("-transparentcolor", 'black')
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

    label = Label(root, text="", font=("Tahoma", 12), bg='black', fg='white', anchor='nw', justify='left')
    label.pack(pady=20, fill='both', expand=True)

    return root, label

def run_overlay():
    root, label = create_overlay()
    root.after(0, update_overlay, root, label)
    root.mainloop()
