#!/usr/bin/python2
import serial
import time
ser = serial.Serial('/dev/ttyACM0',9600,timeout=1.5)
x = ":40f-004-400-004-40f-004-400-004-40f-400-004-400-400-004-400-004;+3:ff0;"
#x = ":+3:0f5;"
for i in range(0,len(x)):
	ser.write(x[i]);
	time.sleep(0.11)
ser.close()
