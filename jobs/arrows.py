import win32con
import time
import main
from jobs import clues, fishing, leveling
from utils import constants, utils

arrow_list = [constants.UP, constants.DOWN, constants.LEFT, constants.RIGHT]

_enabled = False
_camera_back = True

def toggle_arrows():
    global _enabled
    _enabled = not _enabled
    if _enabled:
        clues._enabled = False
        fishing._enabled = False
        leveling._enabled = False

def set_camera_back():
    global _camera_back
    _camera_back = not _camera_back

def do_action(direction):

    def press_arrow(arrow):
        if arrow == constants.UP:
            utils.press_key(win32con.VK_UP)
        elif arrow == constants.DOWN:
            utils.press_key(win32con.VK_DOWN)
        elif arrow == constants.LEFT:
            utils.press_key(win32con.VK_LEFT)
        elif arrow == constants.RIGHT:
            utils.press_key(win32con.VK_RIGHT)

    press_arrow(direction)
    if _camera_back:
        press_arrow(constants.opposite_directions[direction])
    utils.press_key(win32con.VK_ESCAPE)


def check_arrows():
    screenshot = utils.screenshot()
    line_offset = utils.get_sizes('imp2_arrows_height')

    # For each arrow (up, down, left, right)
    for arrow in arrow_list:
        is_recognized = True
        for line_index in range(0, 3):
            y_offset = line_offset * line_index
            # Check 1 red pixel
            coord = utils.get_coordinates('arrows_red')
            if utils.is_color_matching(screenshot, (coord[0], coord[1] + y_offset), constants.colorRGB[constants.COLOR_RED]):
                # Check 4 yellow pixel
                for i in range(1, 5):
                    index = f'arrows_yellow_{arrow}_{i}'
                    coord = utils.get_coordinates(index)
                    if not utils.is_color_matching(screenshot, (coord[0], coord[1] + y_offset), constants.colorRGB[constants.COLOR_YELLOW]):
                        is_recognized = False
                        break
                if is_recognized:
                    do_action(arrow)
                    return

def thread_loop():
    while True:
        if not utils.is_warcraft_active() or not _enabled:
            time.sleep(main.UPDATE_TIME_THREAD)
            continue

        check_arrows()
        time.sleep(0.5)
