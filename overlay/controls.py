from jobs import arrows, clues, fishing, leveling
from overlay import overlay_damage
import keyboard

MENU_MAIN = 'menu_main'
MENU_AUTOMATION = 'menu_automation'
MENU_CLUE = 'menu_clues'
MENU_ARROWS = 'menu_arrows'
MENU_FISHING = 'menu_fishing'
MENU_LEVELING = 'menu_leveling'
MENU_SYSTEM = 'menu_system'
MENU_DAMAGE = 'menu_damage'

CTRL_F1 = 'ctrl+f1'
CTRL_F2 = 'ctrl+f2'
CTRL_F3 = 'ctrl+f3'
CTRL_F4 = 'ctrl+f4'
CTRL_F5 = 'ctrl+f5'
CTRL_F6 = 'ctrl+f6'

# Define the main menu and submenus
controls = {
    MENU_MAIN: {
        CTRL_F1: MENU_AUTOMATION,
        CTRL_F2: MENU_DAMAGE,
        CTRL_F3: MENU_SYSTEM,
    },
    MENU_AUTOMATION: {
        CTRL_F1: MENU_MAIN,
        CTRL_F2: MENU_CLUE,
        CTRL_F3: MENU_ARROWS,
        CTRL_F4: MENU_FISHING,
        CTRL_F5: MENU_LEVELING,
    },
    MENU_CLUE: {
        CTRL_F1: MENU_AUTOMATION,
        CTRL_F2: clues.toggle_clues,
        CTRL_F3: clues.set_clue_mode,
    },
    MENU_ARROWS: {
        CTRL_F1: MENU_AUTOMATION,
        CTRL_F2: arrows.toggle_arrows,
        CTRL_F3: arrows.set_camera_back,
    },
    MENU_FISHING: {
        CTRL_F1: MENU_AUTOMATION,
        CTRL_F2: fishing.toggle_fishing,
        CTRL_F3: fishing.set_fishing_mode,
        CTRL_F4: fishing.set_respawn_point,
        CTRL_F5: fishing.set_fish_save_interval,
    },
    MENU_LEVELING: {
        CTRL_F1: MENU_AUTOMATION,
        CTRL_F2: leveling.toggle_leveling,
        CTRL_F3: leveling.set_click_button,
        CTRL_F4: leveling.set_click_interval,
        CTRL_F5: leveling.set_lvl_save_interval,
    },
    MENU_DAMAGE: {
        CTRL_F1: MENU_MAIN,
        CTRL_F2: overlay_damage.toggle_damage_overlay,
        CTRL_F3: overlay_damage.set_overlay_position,
    },
    MENU_SYSTEM: {
        CTRL_F1: MENU_MAIN,
    }
}

def get_enabled_job():
    if clues._enabled:
        return "(Clues)"
    elif arrows._enabled:
        return "(Arrows)"
    elif fishing._enabled:
        return "(Fishing)"
    elif leveling._enabled:
        return "(Leveling)"
    else:
        return ""

# Custom names for actions
custom_names = {
    MENU_MAIN: lambda: "Main",
    # MENU_AUTOMATION: lambda: f"Automation {get_enabled_job()}",
    MENU_AUTOMATION: lambda: f"Automation {get_enabled_job()}",
    MENU_CLUE: lambda: f"Clues {"(enabled)" if clues._enabled else ""}",
    MENU_ARROWS: lambda: f"Arrows {"(enabled)" if arrows._enabled else ""}",
    MENU_FISHING: lambda: f"Fishing {"(enabled)" if fishing._enabled else ""}",
    MENU_LEVELING: lambda: f"Leveling {"(enabled)" if leveling._enabled else ""}",
    MENU_DAMAGE: lambda: "Damage board",
    MENU_SYSTEM: lambda: "System",
    # Clue
    'toggle_clues': lambda: f"Clue: {"ON" if clues._enabled else "OFF"}" ,
    'set_clue_mode': lambda: f"Print: {"Yes" if clues._print_clue else "No"}",
    # Arrows
    'toggle_arrows': lambda: f"Arrows: {"ON" if arrows._enabled else "OFF"}",
    'set_camera_back': lambda: f"Camera back: {"Yes" if arrows._camera_back else "No"}",
    # Fishing
    'toggle_fishing': lambda: f"Fishing: {"ON" if fishing._enabled else "OFF"}",
    'set_fishing_mode': lambda: f"Fishing mode: {fishing.get_fishing_mode()}",
    'set_respawn_point': lambda: f"Respawn point: {fishing.get_respawn_point_str()}",
    'set_fish_save_interval': lambda: f"Auto-save interval: {f"{fishing.get_save_interval()} min" if fishing.get_save_interval() != None else "none"}",
    # Leveling
    'toggle_leveling': lambda: f"Leveling: {"ON" if leveling._enabled else "OFF"}",
    'set_click_button': lambda: f"Click button: {leveling.get_click_button_str()}",
    'set_click_interval': lambda: f"Click interval: {f"{leveling.get_click_interval()} sec" if leveling.get_click_interval() != None else "none"}",
    'set_lvl_save_interval': lambda: f"Auto-save interval: {f"{leveling.get_save_interval()} min" if leveling.get_save_interval() != None else "none"}",
    # Damage overlay
    'toggle_damage_overlay': lambda: f"Overlay: {"ON" if overlay_damage._enabled else "OFF"}",
    'set_overlay_position': lambda: f"Position: {overlay_damage.get_overlay_position()}",
}

_current_menu = MENU_MAIN

def get_current_menu():
    return _current_menu

def set_current_menu(menu):
    global _current_menu
    _current_menu = menu

def set_hotkeys(menu):
    try:
        keyboard.unhook_all_hotkeys()
    except AttributeError:
        pass
    if menu in controls:
        for hotkey, action in controls[menu].items():
            if isinstance(action, str):
                keyboard.add_hotkey(hotkey, lambda action=action: navigate_to(action))
            else:
                keyboard.add_hotkey(hotkey, action)

def navigate_to(menu):
    set_current_menu(menu)
    set_hotkeys(menu)