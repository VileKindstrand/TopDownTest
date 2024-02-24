import threading
import serial
import time

ser = serial.Serial('COM3', 9600)

def arduino_input():

    i = 0

    while i < 100:      #while true
        arduino_data = ser.readline().decode("utf-8").strip()   
        # Convert the received data to a float
        global sensor_value
        sensor_value = float(arduino_data)
        print (sensor_value)
        i+= 1



def test():
    i = 0
    while i < 100:
        print ("cool")
        i += 1
        time.sleep(1)
y = threading.Thread(target=test, args=())
y.start()