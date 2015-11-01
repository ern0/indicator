#!/usr/bin/python2
import serial
import time
ser = serial.Serial('/dev/ttyACM0', 9600, timeout=0.5)
x = ":400-004-400-004-400-004-400-004-400-400-004-400-400-004-400-004;+3:ff0;"
for i in range(0,len(x)):
	ser.write(x[i]);
	time.sleep(0.01)
ser.close()
