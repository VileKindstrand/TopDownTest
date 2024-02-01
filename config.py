# from data_gather import *
import threading
import serial
import time

WIN_WIDTH = 640
WIN_HEIGHT = 480
TILESIZE = 32
FPS = 60        #egentligen refresh-rate

STANDING_PLAYER = 1, 0, 32, 48
WALK_1_PLAYER = 34, 0, 32, 48
WALK_2_PLAYER = 66, 0, 32, 48

WATER_LEVEL = 100.0
PLAYER_LAYER = 3
BLOCK_LAYER = 2
GROUND_LAYER = 1

PLAYER_SPEED = 3

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
'B....T.............B',
'B..................B',
'B........P.........B',
'B..................B',
'B..................B',
'B..................B',
'B..................B',
'BBBBBBBBBBBBBBBBBBBB',
]


ser = serial.Serial('COM3', 9600)

def arduino_input():

    i = 0

    while i < 100:
        arduino_data = ser.readline().decode("utf-8").strip()   
        # Convert the received data to a float
        global sensor_value
        sensor_value = float(arduino_data)
        print (sensor_value)
        i+= 1

x = threading.Thread(target=arduino_input, args=())
x.start()

def test():
    i = 0
    while i < 100:
        print ("cool")
        i += 1
        time.sleep(1)
y = threading.Thread(target=test, args=())
y.start()