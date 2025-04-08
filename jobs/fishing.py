import pyautogui
import time
import main
from jobs import arrows, clues, leveling
from utils import constants, utils
import datetime
import win32con

MODE_PERFECT = 'Perfect'
MODE_PERFECT_NO_FLY = 'Perfect (no Flying wish fish)'
MODE_GREAT = 'Great'
MODE_STANDARD = 'Standard'
SCORE_LIMIT = 'score_limit'
PERFECT_LOOPS = 'perfect_loops_max'

fishing_modes = [
    MODE_PERFECT,
    MODE_PERFECT_NO_FLY,
    MODE_GREAT,
    MODE_STANDARD
]

fishing_mode_params = {
    MODE_PERFECT: {
        SCORE_LIMIT: 10000,
        PERFECT_LOOPS: 2000
    },
    MODE_PERFECT_NO_FLY: {
        SCORE_LIMIT: 10000,
        PERFECT_LOOPS: 2
    },
    MODE_GREAT: {
        SCORE_LIMIT: 8000,
        PERFECT_LOOPS: 2000
    },
    MODE_STANDARD: {
        SCORE_LIMIT: 5000,
        PERFECT_LOOPS: 2000
    },
}

_enabled = False

arrow_list = [constants.UP, constants.DOWN]
save_interval_options = [None, 5, 10, 30]

fishing_loops = 0
_respawn_point = None
iteration = 0
score = 0
_hero_respawned = True
_save_interval_index = save_interval_options.index(None)
_next_save_time = None


def toggle_fishing():
    global _enabled
    _enabled = not _enabled
    if _enabled:
        set_next_save_time()
        arrows._enabled = False
        clues._enabled = False
        leveling._enabled = False


_current_fishing_mode_index = fishing_modes.index(MODE_PERFECT)

def get_fishing_mode():
    return fishing_modes[_current_fishing_mode_index]

def set_fishing_mode():
    global _current_fishing_mode_index
    _current_fishing_mode_index = (_current_fishing_mode_index + 1) % len(fishing_modes)

def get_fishing_mode_params():
    return fishing_mode_params[get_fishing_mode()]

def get_save_interval():
    return save_interval_options[_save_interval_index]

def set_save_interval():
    global _save_interval_index   #, _next_save_time
    _save_interval_index = (_save_interval_index + 1) % len(save_interval_options)
    set_next_save_time()

def set_next_save_time():
    global _next_save_time
    save_interval = get_save_interval()
    if save_interval != None:
        _next_save_time = datetime.datetime.now() + datetime.timedelta(minutes=save_interval)

def get_respawn_point():
    if _respawn_point != None:
        return utils.get_point(_respawn_point)
    else:
        return None

def set_respawn_point():
    global _respawn_point
    _respawn_point = utils.set_point(pyautogui.position())

def get_respawn_point_str():
    if _respawn_point != None:
        return f'(x={_respawn_point[0]}, y={_respawn_point[1]})'
    else:
        return 'none'

def set_fish_save_interval():
    set_save_interval()

def get_time_to_save():
    if _next_save_time != None:
        if _next_save_time > datetime.datetime.now():
            timedelta = _next_save_time - datetime.datetime.now()
            sec = timedelta.seconds
            hours = sec // 3600
            minutes = (sec // 60) - (hours * 60)
            seconds = sec - (minutes * 60)
            time_str = '{:02d}:{:02d}'.format(minutes, seconds)
        else:
            time_str = 'after the current cycle'

        return time_str
    else:
        return ""

def check_fishing_arrow(screenshot):
    # For each arrow (up, down)
    for arrow in arrow_list:
        is_recognized = True
        # Check 1 pixel inside
        if arrow == constants.UP:
            color = constants.COLOR_YELLOW
        else:
            color = constants.COLOR_GREEN
        coord = utils.get_coordinates(f'fishing_{color}_{arrow}_1')
        if utils.is_color_matching(screenshot, coord, constants.colorRGB[color]):
            # Check 2 white pixels
            for i in range(1, 3):
                coord = utils.get_coordinates(f'fishing_white_{arrow}_{i}')
                if not utils.is_color_matching(screenshot, coord, constants.colorRGB[constants.COLOR_WHITE]):
                    is_recognized = False
                    break
            if is_recognized:
                return arrow
    return None

def is_hero_alive(screenshot):
    coord = utils.get_coordinates('hero_icon_frame')
    result = not utils.is_color_matching(screenshot, coord, constants.colorRGB[constants.COLOR_BLACK])
    return result

def is_hotbar_slot1_active(screenshot):
    coord = utils.get_coordinates('hotbar_slot_1')
    result = not utils.is_color_matching(screenshot, coord, constants.colorRGB[constants.COLOR_BLACK])
    return result

def handle_respawn():
    global _hero_respawned
    while True:
        respawn_point = get_respawn_point()
        if not _enabled or respawn_point is None or _hero_respawned:
            break
        elif not utils.is_warcraft_active():
            time.sleep(0.05)
            continue

        screenshot = utils.screenshot()
        if (is_hero_alive(screenshot) or              # Hero alive
            is_hotbar_slot1_active(screenshot)):      # Hotbar active
            _hero_respawned = True
            if utils._warcraft_foreground:
                utils.press_key(win32con.VK_F1)
                time.sleep(1)
                pyautogui.moveTo(utils.get_coordinates('hotbar_slot_4', True))
                pyautogui.click()
                time.sleep(0.25)
                pyautogui.moveTo(respawn_point)
                pyautogui.click()
            break
        time.sleep(0.5)

def rod_click():
    while True:
        if not _enabled:
            break
        elif not utils.is_warcraft_active():
            time.sleep(0.05)
            continue

        screenshot = utils.screenshot()
        if (not is_hotbar_slot1_active(screenshot)):    # In fishing mode
            break

        utils.press_key(win32con.VK_NUMPAD8)
        time.sleep(2)


def handle_fishing():

    def press_arrow(arrow):
        if arrow == constants.UP:
            utils.press_key(win32con.VK_UP)
        elif arrow == constants.DOWN:
            utils.press_key(win32con.VK_DOWN)

    global fishing_loops, score, iteration, _hero_respawned
    while True:
        if not _enabled:
            break
        elif not utils.is_warcraft_active():
            time.sleep(0.05)
            continue

        screenshot = utils.screenshot()
        if not is_hero_alive(screenshot):         # Hero died
            _hero_respawned = False
            break
        if is_hotbar_slot1_active(screenshot):    # Fishing cycle finished
            break

        arrow = check_fishing_arrow(screenshot)
        if arrow != None:
            # Fail first try when reached number of perfect loops
            if fishing_loops >= get_fishing_mode_params()[PERFECT_LOOPS]:
                press_arrow(constants.opposite_directions[arrow])
                fishing_loops = -1
            # Score reached
            elif score >= get_fishing_mode_params()[SCORE_LIMIT]:
                press_arrow(constants.opposite_directions[arrow])
            else:
                press_arrow(arrow)
                score += 500
            iteration += 1

        time.sleep(0.4)

    if score > 0:
        fishing_loops += 1
    iteration = 0
    score = 0

def handle_save():
    if utils.is_warcraft_active() and _enabled:
        if get_save_interval() != None and _next_save_time != None:
            if datetime.datetime.now() >= _next_save_time:
                set_next_save_time()
                utils.press_key(win32con.VK_RETURN)
                utils.send_string('-s')
                utils.press_key(win32con.VK_RETURN)

def thread_loop():
    while True:
        if not utils.is_warcraft_active() or not _enabled:
            time.sleep(main.UPDATE_TIME_THREAD)
            continue

        handle_respawn()
        rod_click()
        handle_fishing()
        handle_save()
        time.sleep(1)      # iteration pause
