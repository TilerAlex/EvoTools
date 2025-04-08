import pygetwindow
from win32 import win32gui, win32process, win32api
import win32con
import win32ui
from PIL import Image
from utils import constants
import psutil
from ctypes import windll

debug_mode = False
_warcraft_active = False
_warcraft_foreground = False
_resolution = ""
_x = 0
_y = 0
_width = 0
_height = 0
_window_handle = None


def is_color_matching(screenshot, coord, color):
    try:
        pixel = screenshot.getpixel((coord[0], coord[1]))
    except IndexError:     # image index out of range
        return False
    return pixel == color

def mouse_click(button, pos):
    if _window_handle != None:
        x, y = pos
        coords = win32api.MAKELONG(x, y)
        # win32api.SendMessage(_window_handle, win32con.WM_ACTIVATE, win32con.WA_ACTIVE, 0)
        win32api.SendMessage(_window_handle, win32con.WM_MOUSEMOVE, 0, coords)
        win32api.SendMessage(_window_handle, win32con.WM_LBUTTONDOWN, button, coords)
        win32api.SendMessage(_window_handle, win32con.WM_LBUTTONUP, button, coords)

def press_key(key):
    if _window_handle != None:
        win32api.SendMessage(_window_handle, win32con.WM_KEYDOWN, key, 0)
        win32api.SendMessage(_window_handle, win32con.WM_KEYUP, key, 0)

def press_letter(key):
    if _window_handle != None:
        key_code = win32api.VkKeyScan(key)
        win32api.SendMessage(_window_handle, win32con.WM_KEYDOWN, key_code, 0)
        win32api.SendMessage(_window_handle, win32con.WM_KEYUP, key_code, 0)

def send_string(str):
    if _window_handle != None:
        for c in str:
            if c == "\n":
                win32api.SendMessage(_window_handle, win32con.WM_KEYDOWN, win32con.VK_RETURN, 0)
                win32api.SendMessage(_window_handle, win32con.WM_KEYUP, win32con.VK_RETURN, 0)
            else:
                win32api.SendMessage(_window_handle, win32con.WM_CHAR, ord(c), 0)


def is_warcraft_active():
    return _warcraft_active

def set_warcraft_foreground():
    win32gui.SetForegroundWindow(_window_handle)

def get_warcraft_data():
    global _window_handle, _warcraft_active, _warcraft_foreground   # _window

    if _window_handle is None:
        active_window = pygetwindow.getActiveWindow()
        if not active_window:
            return
        window_handle = active_window._hWnd

        thread_id, process_id = win32process.GetWindowThreadProcessId(window_handle)
        process = psutil.Process(process_id)
        if process.name() == "Warcraft III.exe":
            _window_handle = window_handle
            _warcraft_active = True
            _warcraft_foreground = True
    else:
        if win32gui.IsWindow(_window_handle):
            tup = win32gui.GetWindowPlacement(_window_handle)
            # print('tup[1]:', tup[1])
            if tup[1] == win32con.SW_SHOWMINIMIZED:
                _warcraft_active = False
            else:
                _warcraft_active = True
            _warcraft_foreground = win32gui.GetForegroundWindow() == _window_handle
        else:
            _window_handle = None
            _warcraft_active = False
            _warcraft_foreground = False

    if _warcraft_active:
        update_resolution(_window_handle)

def update_resolution(window_handle):
    global _resolution, _x, _y, _width, _height

    if window_handle is None:
        return

    # Game resolution
    rect_left, rect_top, rect_right, rect_bottom = win32gui.GetClientRect(window_handle)
    _width = rect_right - rect_left
    _height = rect_bottom - rect_top

    # Window offset
    _x, _y = win32gui.ClientToScreen(window_handle, (0, 0))

    _resolution = f"{_width}x{_height}"

def screenshot():
    if _window_handle is None:
        return None

    # Consider high DPI display or > 100% scaling size
    windll.user32.SetProcessDPIAware()

    left, top, right, bot = win32gui.GetClientRect(_window_handle)
    w = right - left
    h = bot - top

    hwndDC = win32gui.GetWindowDC(_window_handle)
    mfcDC  = win32ui.CreateDCFromHandle(hwndDC)
    saveDC = mfcDC.CreateCompatibleDC()

    saveBitMap = win32ui.CreateBitmap()
    saveBitMap.CreateCompatibleBitmap(mfcDC, w, h)

    saveDC.SelectObject(saveBitMap)

    result = windll.user32.PrintWindow(_window_handle, saveDC.GetSafeHdc(), 1)

    bmpinfo = saveBitMap.GetInfo()
    bmpstr = saveBitMap.GetBitmapBits(True)

    try:
        im = Image.frombuffer(
            'RGB',
            (bmpinfo['bmWidth'], bmpinfo['bmHeight']),
            bmpstr, 'raw', 'BGRX', 0, 1)
    except ValueError:
        im = Image.new('RGB', (1, 1))
        pass

    win32gui.DeleteObject(saveBitMap.GetHandle())
    saveDC.DeleteDC()
    mfcDC.DeleteDC()
    win32gui.ReleaseDC(_window_handle, hwndDC)

    return im

def get_point(coord):
    x, y = coord
    if _x != 0 or _y != 0:
        x += _x
        y += _y
    return (x, y)

def set_point(coord):
    x, y = coord
    if _x != 0 or _y != 0:
        x -= _x
        y -= _y
    return (x, y)

def get_coordinates(index, adjust=False):
    try:
        coord = constants.coordinates[_resolution][index]
        # Consider window offset
        if adjust and (_x != 0 or _y != 0):
            coord = (coord[0] + _x, coord[1] + _y)
        return coord
    except:
        return (0, 0)
        # pass

def get_sizes(index):
    try:
        return constants.sizes[_resolution][index]
    except:
        return 0
        # pass
