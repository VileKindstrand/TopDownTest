# from data_gather import *
import threading
import serial
import time
import pygame

WIN_WIDTH = 640
WIN_HEIGHT = 480
TILESIZE = 64
FPS = 60        #egentligen refresh-rate

PLAYER_HEIGHT = TILESIZE*1.5
PLAYER_WIDTH = TILESIZE

SPRITESHEET_WIDTH = 32
SPRITESHEET_HEIGTH = 32

FIRST_WATER_LEVEL = 100.0
FIRST_PLAYER_HP = 100.0
WATER_EXCHANGE = 1

TEXT_BOX_LAYER = 5
PLAYER_LAYER = 4
NPC_LAYER = 3
BLOCK_LAYER = 2
GROUND_LAYER = 1

PLAYER_SPEED = 6
ENEMY_SPEED = 2
ENEMY_HUNTING_SPEED = ENEMY_SPEED*2

RED = (255, 0, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)


tilemap = [

'BBBBBBBBBBBBBBBBBBBB',
'BTTTBBBBBBBBTTTTTTTB',
'B...TTTTTTTT.......B',
'B..................B',
'B..............B...B',
'B..............T...B',
'B....B.............B',
'B....T.......E.....B',
'B..................B',
'B........P.........B',
'B..................B',
'B....K.............B',
'B..................B',
'B..................B',
'BBBBBBBBBBBBBBBBBBBB',
]

