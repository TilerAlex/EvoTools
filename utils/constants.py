RES_1080 = '1920x1080'
RES_1440 = '2560x1440'

JOB_ARROWS = 'arrows'
JOB_CLUES = 'clue'
JOB_FISHING = 'fishing'

UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'

ARROW_UP = 'up'
ARROW_DOWN = 'down'
ARROW_LEFT = 'left'
ARROW_RIGHT = 'right'

TOP_LEFT = 'top_left'
TOP_RIGHT = 'top_right'
BOT_LEFT = 'bot_left'
BOT_RIGHT = 'bot_right'

COLOR_GREEN = 'green'
COLOR_RED = 'red'
COLOR_BLACK = 'black'
COLOR_YELLOW = 'yellow'
COLOR_WHITE = 'white'
COLOR_BLUE = 'blue'

# def get_coordinate(job, color, value, index):
#     return f'{job}{color}{value}{index}'

coordinates = {
    RES_1440: {
        # get_coordinate(JOB_ARROWS, COLOR_YELLOW, ARROW_UP, 1): (450, 770),
        # ARROWS
        # f'{JOB_ARROWS}{COLOR_RED}': (0, 0),
        # f'{JOB_ARROWS}{COLOR_YELLOW}{ARROW_UP}{1}': (0, 0),
        # f'{JOB_ARROWS}{COLOR_YELLOW}{ARROW_UP}{2}': (0, 0),
        'arrows_red': (450, 770),              # D
        'arrows_yellow_up_1': (625, 770),      # U
        'arrows_yellow_up_2': (634, 770),      # P
        'arrows_yellow_up_3': (669, 761),      # A
        'arrows_yellow_up_4': (685, 761),      # R
        'arrows_yellow_down_1': (626, 770),    # D
        'arrows_yellow_down_2': (633, 770),    # O
        'arrows_yellow_down_3': (675, 764),    # W
        'arrows_yellow_down_4': (695, 762),    # N
        'arrows_yellow_left_1': (619, 781),    # L
        'arrows_yellow_left_2': (628, 781),    # E
        'arrows_yellow_left_3': (646, 770),    # F
        'arrows_yellow_left_4': (664, 775),    # T
        'arrows_yellow_right_1': (609, 781),   # R
        'arrows_yellow_right_2': (629, 770),   # I
        'arrows_yellow_right_3': (656, 775),   # G
        'arrows_yellow_right_4': (682, 770),   # H
        # CLUES
        # Top Left
        'clue_blue_top_left_1': (450, 843),      # 1
        'clue_green_top_left_1_1': (768, 833),
        'clue_green_top_left_1_2': (796, 833),
        'clue_green_top_left_1_3': (896, 833),
        'clue_blue_top_left_2': (450, 807),      # 2
        'clue_green_top_left_2_1': (1526, 797),
        'clue_green_top_left_2_2': (1541, 797),
        'clue_green_top_left_2_3': (1596, 797),
        # Top Right
        'clue_blue_top_right_1': (450, 843),     # 1
        'clue_green_top_right_1_1': (702, 833),
        'clue_green_top_right_1_2': (718, 833),
        'clue_green_top_right_1_3': (846, 833),
        'clue_blue_top_right_2': (450, 807),     # 2
        'clue_green_top_right_2_1': (1370, 797),
        'clue_green_top_right_2_2': (1387, 797),
        'clue_green_top_right_2_3': (1568, 797),
        # Bot Left
        'clue_blue_bot_left_1': (450, 807),      # 2
        'clue_green_bot_left_1_1': (1528, 797),
        'clue_green_bot_left_1_2': (1536, 797),
        'clue_green_bot_left_1_3': (1564, 797),
        'clue_blue_bot_left_2': (450, 771),      # 3
        'clue_green_bot_left_2_1': (1301, 761),
        'clue_green_bot_left_2_2': (1414, 761),
        'clue_green_bot_left_2_3': (1512, 761),
        # Bot Right
        'clue_blue_bot_right_1': (450, 843),     # 1
        'clue_green_bot_right_1_1': (567, 833),
        'clue_green_bot_right_1_2': (675, 833),
        'clue_green_bot_right_1_3': (777, 833),
        'clue_blue_bot_right_2': (450, 843),     # 1
        'clue_green_bot_right_2_1': (1020, 833),
        'clue_green_bot_right_2_2': (1110, 833),
        'clue_green_bot_right_2_3': (1196, 833),
        # Fishing
        'fishing_yellow_up_1': (734, 832),    # O
        'fishing_white_up_1': (598, 832),     # [
        'fishing_white_up_2': (860, 832),     # ]
        'fishing_green_down_1': (802, 832),   # O
        'fishing_white_down_1': (598, 832),   # [
        'fishing_white_down_2': (928, 832),   # [
        # Common
        'hero_icon': (55, 115),
        'hero_icon_frame': (15, 70),      # hero icon frame becomes black when hero is dead
        'hotbar_slot_1': (1860, 1150),
        'hotbar_slot_4': (2165, 1170),
        # 'character_alive': (1280, 1197),
        'fish_drop': (1603, 1222),     # slot 1
        # Inventory
        'inv_item_1': (1600, 1200),
        'inv_item_2': (1700, 1200),
        'inv_item_3': (1600, 1300),
        'inv_item_4': (1700, 1300),
        'inv_item_5': (1600, 1400),
        'inv_item_6': (1700, 1400),
    },
    RES_1080: {
        # Arrows
        'arrows_red': (338, 579),              # D
        'arrows_yellow_up_1': (455, 580),
        'arrows_yellow_up_2': (475, 580),
        'arrows_yellow_up_3': (483, 573),
        'arrows_yellow_up_4': (493, 585),
        'arrows_yellow_down_1': (456, 570),
        'arrows_yellow_down_2': (482, 570),
        'arrows_yellow_down_3': (493, 571),
        'arrows_yellow_down_4': (525, 577),
        'arrows_yellow_left_1': (462, 586),
        'arrows_yellow_left_2': (475, 570),
        'arrows_yellow_left_3': (474, 586),
        'arrows_yellow_left_4': (482, 580),
        'arrows_yellow_right_1': (463, 583),
        'arrows_yellow_right_2': (471, 580),
        'arrows_yellow_right_3': (477, 578),
        'arrows_yellow_right_4': (491, 581),
        # CLUES
        # Top Left
        'clue_blue_top_left_1': (337, 632),      # 1
        'clue_green_top_left_1_1': (572, 624),
        'clue_green_top_left_1_2': (616, 624),
        'clue_green_top_left_1_3': (666, 624),
        'clue_blue_top_left_2': (337, 605),      # 2
        'clue_green_top_left_2_1': (1133, 597),
        'clue_green_top_left_2_2': (1145, 597),
        'clue_green_top_left_2_3': (1186, 597),
        # Top Right
        'clue_blue_top_right_1': (337, 632),     # 1
        'clue_green_top_right_1_1': (526, 624),
        'clue_green_top_right_1_2': (537, 624),
        'clue_green_top_right_1_3': (633, 624),
        'clue_blue_top_right_2': (337, 605),     # 2
        'clue_green_top_right_2_1': (1018, 597),
        'clue_green_top_right_2_2': (1030, 597),
        'clue_green_top_right_2_3': (1185, 597),
        # Bot Left
        'clue_blue_bot_left_1': (337, 605),      # 2
        'clue_green_bot_left_1_1': (1061, 601),
        'clue_green_bot_left_1_2': (1135, 601),
        'clue_green_bot_left_1_3': (1161, 601),
        'clue_blue_bot_left_2': (337, 578),      # 3
        'clue_green_bot_left_2_1': (913, 573),
        'clue_green_bot_left_2_2': (964, 573),
        'clue_green_bot_left_2_3': (1044, 573),
        # Bot Right
        'clue_blue_bot_right_1': (337, 632),     # 1
        'clue_green_bot_right_1_1': (522, 624),
        'clue_green_bot_right_1_2': (546, 624),
        'clue_green_bot_right_1_3': (570, 624),
        'clue_blue_bot_right_2': (337, 632),     # 1
        'clue_green_bot_right_2_1': (824, 624),
        'clue_green_bot_right_2_2': (845, 624),
        'clue_green_bot_right_2_3': (887, 624),
        # Fishing
        'fishing_yellow_up_1': (546, 624),    # O
        'fishing_white_up_1': (444, 624),     # [
        'fishing_white_up_2': (639, 624),     # ]
        'fishing_green_down_1': (597, 624),   # O
        'fishing_white_down_1': (444, 624),   # [
        'fishing_white_down_2': (690, 624),   # [
        # Common
        'hero_icon': (40, 80),
        'hero_icon_frame': (11, 50),      # hero icon frame becomes black when hero is dead
        'hotbar_slot_1': (1395, 860),
        'hotbar_slot_4': (1620, 875),
        # 'character_alive': (960, 897),
        'fish_drop': (1603, 1222),     # slot 1
        # Inventory
        'inv_item_1': (1600, 1200),
        'inv_item_2': (1700, 1200),
        'inv_item_3': (1600, 1300),
        'inv_item_4': (1700, 1300),
        'inv_item_5': (1600, 1400),
        'inv_item_6': (1700, 1400),
    },
}

sizes = {
    RES_1440: {
        'imp2_arrows_height': 36
    },
    RES_1080: {
        'imp2_arrows_height': 27
    },
}

colorRGB = {
    COLOR_GREEN: (0, 255, 0),         # Green
    COLOR_RED: (255, 0, 0),           # Red
    COLOR_BLACK: (0, 0, 0),           # Black
    COLOR_YELLOW: (255, 204, 0),      # Yellow
    COLOR_WHITE: (255, 255, 255),     # White
    COLOR_BLUE: (135, 206, 235),      # Blue (clue Imp1)
}

opposite_directions = {
    'down': 'up',
    'up': 'down',
    'left': 'right',
    'right': 'left'
}
