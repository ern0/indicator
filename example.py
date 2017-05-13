#!/usr/bin/env python2
import serial
import time
import sys

cmd = '*30:000-f0f-fff-ccc-fff;'

crlf = False
while True:
	try:
		#ser = serial.Serial('/dev/ttyACM0',9600,timeout=2)
		ser = serial.Serial('/dev/tty.wchusbserial1410',38400,timeout=2)
	except:
		sys.stderr.write(".")
		crlf = True
		time.sleep(0.5)
		continue
	break
if crlf: sys.stderr.write("\n")


ser.write(cmd)
time.sleep(4)
ser.close()
