from utils import utils
from overlay import controls, overlay
from jobs import arrows, clues, fishing, leveling
import threading
import pyautogui
import time
import sys

pyautogui.FAILSAFE = False

VERSION = '1.0'
UPDATE_TIME_THREAD = 0.05

if __name__ == "__main__":

    # Init Controls
    controls.set_hotkeys(controls.get_current_menu())

    # Overlay thread
    overlay_thread = threading.Thread(target=overlay.run_overlay, daemon=True)
    overlay_thread.start()

    # Arrows thread
    arrows_thread = threading.Thread(target=arrows.thread_loop, daemon=True)
    arrows_thread.start()

    # Clue thread
    clue_thread = threading.Thread(target=clues.thread_loop, daemon=True)
    clue_thread.start()

    # Fishing thread
    fishing_thread = threading.Thread(target=fishing.thread_loop, daemon=True)
    fishing_thread.start()

    # Leveling thread
    leveling_thread = threading.Thread(target=leveling.thread_loop, daemon=True)
    leveling_thread.start()

    # Button thread
    button_thread = threading.Thread(target=leveling.button_loop, daemon=True)
    button_thread.start()

    print(f"Evo Tools {VERSION} started")

    try:
        while True:
            utils.get_warcraft_data()
            time.sleep(0.25)
    except KeyboardInterrupt:
        sys.exit("Evo Tools stopped")
