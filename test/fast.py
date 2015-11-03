#!/usr/bin/python2
import serial
import time
import sys

crlf = False
while True:
	try:
		ser = serial.Serial('/dev/ttyACM0',9600,timeout=2)
	except:
		sys.stderr.write(".")
		crlf = True
		time.sleep(0.5)
		continue
	break
if crlf: sys.stderr.write("\n")

x = "*5:c40-c22-c44-c66-66c-44c-22c-04c-0c0-2c2-4c4-6c6-cc6-cc4-cc2-cc4;"


for i in range(0,len(x)):
	ser.write(x[i]);
	sys.stderr.write("  " + str(1 + i) + "/" + str(len(x)) + "\r")
ser.close()

sys.stderr.write("\n")
