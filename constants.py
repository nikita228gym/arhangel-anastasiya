"""Базовые константы игры."""

# Настройки экрана
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
FPS = 60
TITLE = "Тактический 2D шутер"

# Размеры мира
TILE_SIZE = 64

# Цвета
COLOR_BG = (25, 25, 30)
COLOR_WALL = (70, 70, 80)
COLOR_GRID = (40, 40, 50)
COLOR_BLUE = (70, 130, 255)
COLOR_RED = (235, 80, 90)
COLOR_TEXT = (240, 240, 240)
COLOR_BUTTON = (65, 65, 80)
COLOR_BUTTON_HOVER = (90, 90, 120)
COLOR_BULLET = (255, 210, 70)
COLOR_HP_BG = (60, 20, 20)
COLOR_HP_FG = (70, 220, 90)
COLOR_FOV = (255, 255, 140, 70)

# Настройки игроков
PLAYER_RADIUS = 18
PLAYER_SPEED = 210
PLAYER_HP = 100

# Настройки обзора
FOV_ANGLE = 90
FOV_RANGE = 420
RAY_STEP = 10

# Настройки раунда
ROUND_PREPARE_SECONDS = 0.1
TEAM_BLUE = "blue"
TEAM_RED = "red"

# Карты
MAP_NAMES = ["map1", "map2"]

# Оружие
WEAPON_PISTOL = "Пистолет"
WEAPON_RIFLE = "Автомат"

# Настройки ИИ
BOT_PATROL_WAIT = 0.5
BOT_CHASE_DISTANCE = 520
BOT_ATTACK_DISTANCE = 380
