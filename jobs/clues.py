import time
import main
import win32con
from jobs import arrows, fishing, leveling
from utils import constants, utils

pos_list = [constants.TOP_LEFT, constants.TOP_RIGHT, constants.BOT_LEFT, constants.BOT_RIGHT]
pos_to_word = {
    constants.TOP_LEFT: 'Top Left',
    constants.TOP_RIGHT: 'Top Right',
    constants.BOT_LEFT: 'Bot Left',
    constants.BOT_RIGHT: 'Bot Right'
}

_enabled = False
_print_clue = False
_last_clue = None


def toggle_clues():
    global _enabled
    _enabled = not _enabled
    if _enabled:
        arrows._enabled = False
        fishing._enabled = False
        leveling._enabled = False

def get_last_pos_str():
    if _last_clue != None:
        return pos_to_word[_last_clue]
    return ''

def set_clue_mode():
    global _print_clue
    _print_clue = not _print_clue

def do_action(pos):
    if _print_clue:
        utils.press_key(win32con.VK_RETURN)
        utils.send_string(pos)
        utils.press_key(win32con.VK_RETURN)
    utils.press_key(win32con.VK_ESCAPE)

def check_clue():
    screenshot = utils.screenshot()

    # For each position (top_left, top_right, bot_left, bot_right)
    for pos in pos_list:
        # Check two options
        for option in range(1, 3):
            is_recognized = True
            # Check 1 blue pixel
            coord = utils.get_coordinates(f'clue_blue_{pos}_{option}')
            if utils.is_color_matching(screenshot, coord, constants.colorRGB[constants.COLOR_BLUE]):
                # Check 4 green pixel
                for i in range(1, 4):
                    coord = utils.get_coordinates(f'clue_green_{pos}_{option}_{i}')
                    if not utils.is_color_matching(screenshot, coord, constants.colorRGB[constants.COLOR_GREEN]):
                        is_recognized = False
                        break
                if is_recognized:
                    # print('is_recognized true')
                    global _last_clue
                    _last_clue = pos
                    do_action(get_last_pos_str())
                    return

def thread_loop():
    while True:
        if not utils.is_warcraft_active() or not _enabled:
            time.sleep(main.UPDATE_TIME_THREAD)
            continue

        check_clue()
        time.sleep(0.5)    # iteration pause
