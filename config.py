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
PROJECTILE_WIDTH = TILESIZE / 2
PROJECTILE_HEIGHT = TILESIZE / 2

FIRST_WATER_LEVEL = 200.0
FIRST_PLAYER_HP = 20.0
WATER_EXCHANGE = 0.1
ATTACK_COST = 2
ENEMY_DAMAGE = 0.2
SPAWN_RATE = 0.25

TEXT_BOX_LAYER = 5
PLAYER_LAYER = 4
NPC_LAYER = 3
BLOCK_LAYER = 2
GROUND_LAYER = 1

PROJECTILE_SPEED = TILESIZE / 4
PLAYER_SPEED = TILESIZE / 10
ENEMY_SPEED = TILESIZE / 48
ENEMY_DRY_SPEED = ENEMY_SPEED * 1.25

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
'B.....P........T...B',
'B....B.............B',
'B....T....W........B',
'B..................B',
'B..................B',
'B..................B',
'B....K.............B',
'B..................B',
'B..................B',
'BBBBBBBBBBBBBBBBBBBB',
]

