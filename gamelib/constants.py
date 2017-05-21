import math
from pyglet.window import key

MAX_FRAME_RATE = 60
MIN_FRAME_RATE = 15
TIME_STEP = (1.0 / MAX_FRAME_RATE)
TIME_STEP_SQ = TIME_STEP * TIME_STEP
MAX_CYCLES_PER_FRAME = (MAX_FRAME_RATE / MIN_FRAME_RATE)

# RES LIMITS
WIDTH = 800
HEIGHT = 600

# SCROLLING
MAX_COPTER_REL_X = WIDTH/2
MIN_SCROLL_SPEED = 200.0

# PHYSICS
GRAVITY = -980

# HELICOPTER
HELI_POWER = 1500
HELI_DAMPENING = 0.95

# ROPE
ROPE_SEGMENTS = 15
ROPE_SEGMENT_LENTH = 9.6
ROPE_DAMPENING = 0.96
ROPE_RELAXATION = 2

BULLET_POOL = 50
ENEMY_POOL = 50

PLAYER_BULLET_SPEED = 900
ENEMY_BULLET_SPEED = 300



# GAME KEYS
HELI_UP =    key.UP
HELI_DOWN =  key.DOWN
HELI_LEFT =  key.LEFT
HELI_RIGHT = key.RIGHT
FIRE_UP =    key.W
FIRE_DOWN =  key.S
FIRE_LEFT =  key.A
FIRE_RIGHT = key.D


# angle lookup table
DIR_U =  math.sin(math.radians(0)),   math.cos(math.radians(0)),   0
DIR_UR = math.sin(math.radians(45)),  math.cos(math.radians(45)),  45
DIR_R =  math.sin(math.radians(90)),  math.cos(math.radians(90)),  90
DIR_DR = math.sin(math.radians(135)), math.cos(math.radians(135)), 135
DIR_D =  math.sin(math.radians(180)), math.cos(math.radians(180)), 180
DIR_DL = math.sin(math.radians(225)), math.cos(math.radians(225)), 225
DIR_L =  math.sin(math.radians(270)), math.cos(math.radians(270)), 270
DIR_UL = math.sin(math.radians(315)), math.cos(math.radians(315)), 315