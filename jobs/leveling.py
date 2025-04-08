import time
import datetime
import main
from jobs import arrows, clues, fishing
from utils import utils
import win32con
import keyboard

_enabled = False

click_interval_options = [None, 1, 2, 3]
save_interval_options = [None, 5, 10, 30]

_click_button = None
_click_button_input = False
_click_interval_index = click_interval_options.index(2)
_save_interval_index = save_interval_options.index(None)
_next_click_time = None
_next_save_time = None

def toggle_leveling():
    global _enabled
    _enabled = not _enabled
    if _enabled:
        set_next_click_time()
        set_next_save_time()
        arrows._enabled = False
        clues._enabled = False
        fishing._enabled = False

def get_click_button_str():
    if _click_button_input:
        return '(press button or ESC to clear)'
    else:
        if _click_button is None:
            return ('none')
        else:
            return _click_button.upper()

def set_click_button():
    global _click_button, _click_button_input
    _click_button_input = True

def set_next_click_time():
    global _next_click_time
    click_interval = get_click_interval()
    if click_interval != None:
        _next_click_time = datetime.datetime.now() + datetime.timedelta(seconds=click_interval)

def set_next_save_time():
    global _next_save_time
    save_interval = get_save_interval()
    if save_interval != None:
        _next_save_time = datetime.datetime.now() + datetime.timedelta(minutes=save_interval)

def get_time_to_save():
    if _next_save_time != None:
        timedelta = _next_save_time - datetime.datetime.now()
        sec = timedelta.seconds
        hours = sec // 3600
        minutes = (sec // 60) - (hours * 60)
        seconds = sec - (minutes * 60)
        return '{:02d}:{:02d}'.format(minutes, seconds)
    else:
        return ""

def get_click_interval():
    return click_interval_options[_click_interval_index]

def set_click_interval():
    global _click_interval_index
    _click_interval_index = (_click_interval_index + 1) % len(click_interval_options)
    set_next_click_time()

def get_save_interval():
    return save_interval_options[_save_interval_index]

def set_save_interval():
    global _save_interval_index   #, _next_save_time
    _save_interval_index = (_save_interval_index + 1) % len(save_interval_options)
    set_next_save_time()

def set_lvl_save_interval():
    set_save_interval()

def clicking_loop():
    global _click_button
    if utils.is_warcraft_active():
        if _click_button != None and get_click_interval() != None and _next_click_time != None:
            if datetime.datetime.now() >= _next_click_time:
                utils.press_letter(_click_button)
                set_next_click_time()

def saving_loop():
    if utils.is_warcraft_active():
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

        clicking_loop()
        saving_loop()
        time.sleep(0.05)   # iteration pause

def button_loop():
    global _click_button, _click_button_input
    while True:
        if not utils.is_warcraft_active():
            time.sleep(main.UPDATE_TIME_THREAD)
            continue

        if _click_button_input:
            time.sleep(0.25)
            key = keyboard.read_key()
            if key != None and len(key) == 1 and key.isalpha():
                _click_button = key
                _click_button_input = False
            elif key == 'esc':
                _click_button = None
                _click_button_input = False

        time.sleep(0.1)    # iteration pause
