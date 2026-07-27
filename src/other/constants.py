import cv2
import numpy as np

# ==========================================
# 1. User & Game Statistics
# ==========================================
FULL_HP = 100
FULL_MP = 100
FULL_LEVEL = 999
FULL_EXP = 100
FULL_ATTACK = 999
MAIN_USER_NAME = "Greedy Dreamer"

# ==========================================
# 2. UI & Styling (Colors)
# ==========================================
# HUD Bar Colors
MP_OUTER_COLOR = (255, 31, 0)
MP_INNER_COLOR = (255, 150, 150)
HP_OUTER_COLOR = (0, 31, 255)
HP_INNER_COLOR = (150, 150, 255)
EXP_OUTER_COLOR = (0, 150, 0)
EXP_INNER_COLOR = (57, 255, 20)
DEFAULT_BAR_COLOR = (100, 100, 100)

# Label/Rectangle Colors
TEXT_OUTER_COLOR = (0, 200, 0)
TEXT_INNER_COLOR = (150, 255, 150)
BD_OUTER_COLOR = (0, 200, 0)
BD_INNER_COLOR = (150, 255, 150)
BG_COLOR = (0, 60, 0)
REG_OUTER_BG_COLOR = (40, 30, 10)
REG_OUTER_BD_COLOR = (90, 70, 20)
SEL_OUTER_BG_COLOR = (85, 60, 15)
SEL_OUTER_BD_COLOR = (255, 230, 0)
BG_REGULAR_RECTANGLE = (80, 80, 80)
BG_SELECTED_RECTANGLE = (255, 0, 180)
BD_REGULAR_RECTANGLE = (100, 100, 100)
BD_SELECTED_RECTANGLE = (255, 0, 255)

# Death & Haki Colors
DEATH_OUTER_COLOR = (20, 20, 200)
DEATH_INNER_COLOR = (180, 180, 255)
DEATH_BG = (63, 63, 154)
HAKI_CORE = (10, 10, 10)
HAKI_MIDDLE = (140, 0, 120)
HAKI_OUTER = (255, 100, 255)

# ==========================================
# 3. UI & Styling (Layout & Geometry)
# ==========================================
OTHER_BAR_LENGTH = 50
OTHER_BAR_THICK = 5
MAIN_EXP_BAR = (620, 350)
MAIN_HUD_TOP_LEFT = (480, 10)
MAIN_HOR_BAR_LENGTH = 80
MAIN_HOR_BAR_THICK = 5
MAIN_VER_BAR_LENGTH = 200
MAIN_VER_BAR_THICK = 5
MAIN_IMAGE_WIDTH = 40
MAIN_IMAGE_HEIGHT = 40

FONT_FACE = cv2.FONT_HERSHEY_SIMPLEX
NAME_SCALE = 0.6
NAME_THICKNESS = 1
LEVEL_SCALE = 0.4
LEVEL_THICKNESS = 1
PADDING = 4
LINE_SPACE = 10
CORNER_BAR_THICKNESS = 2
CONNECTOR_LENGTH = 20
ADDITIONAL_SIZE = 5

# ==========================================
# 4. Computer Vision & ML Configuration
# ==========================================
YOLO_MODEL_PATH = "./weights/segmentation.pt"
RECOGNITION_IMAGES_PATH = "./assets/identity"
RECOGNITION_THRESHOLD = 50
RECOGNITION_INTERVAL = 20 
MAX_AGE = 20
MIN_HITS = 3
IOU_THRESHOLD = 0.4

# Processing Filters
DILATE_KERNEL = np.ones((3, 3), np.uint8)
DILATE_ALPHA = 0.7
DILATE_BETA = 1
DILATE_GAMMA = 0
DILATE_ITERATION = 1
BLUR_KERNEL = (15, 15)
TRANS_ALPHA = 0.6
TRANS_BETA = 1 - TRANS_ALPHA
TRANS_GAMMA = 0

# ==========================================
# 5. Hand & Gesture Tracking
# ==========================================
MEDIAPIPE_PATH = "./weights/hand_landmarker.task"
HAND_CONNECTIONS = [
    (0, 1), (1, 2), (2, 3), (3, 4), 
    (0, 5), (5, 6), (6, 7), (7, 8), 
    (5, 9), (9, 10), (10, 11), (11, 12), 
    (9, 13), (13, 14), (14, 15), (15, 16), 
    (13, 17), (0, 17), (17, 18), (18, 19), (19, 20)
]
HAND_LINE_COLOR = (0, 255, 0)
HAND_POINT_COLOR = (255, 0, 0)
HAND_POINT_SCALE = 5
LSTM_LABEL_MAP = ["any", "click", "fire", "gun_pose", "open_palm"]
LSTM_WEIGHT_FILE = "./weights/action.h5"

# ==========================================
# 6. Items & Equipment
# ==========================================
GUN_STEP = 10
GUN_NAME = "gun"
GUN_DAMAGE = 6
GUN_IMAGE_LINK = "./assets/item/ball.png"
EXPLODE_PROJECTILE = "./assets/item/explode.png"

KATANA_NAME = "katana"
KATANA_DAMAGE = 4
KATANA_IMAGE_LINK = "./assets/item/katana.png"

HAND_NAME = "hand"
HAND_DAMAGE = 1
HAND_IMAGE_LINK = "./assets/item/hand.png"

POTION_NAME = "potion"
POTION_DAMAGE = 4
POTION_IMAGE_LINK = "./assets/item/potion.png"

PROPOTION_LENGTH_CONNECTOR = 6 
DEATH_IMAGE = "./assets/item/death.png"
ITEM_BAR_THICK = 2
LIST_ITEM__SIZE = (60, 60)
TOP_LEFT_ITEMS_LIST = (320 - 120, 240 - 30)
OPEN_LIST = True
CLOSE_LIST = False

# ==========================================
# 7. Visual Effects (Damage)
# ==========================================
AURA_INTENSITY = 0.7   
DAMAGE_COLORS_BGR = [
    (255, 255, 255),
    (0, 85, 255),
    (0, 0, 255),
    (0, 0, 200),
    (0, 0, 140),
    (0, 0, 80),
]
