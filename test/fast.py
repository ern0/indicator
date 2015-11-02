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

x = ":00f-0f0-f00-ccc-aca-877-300-990;"

for i in range(0,len(x)):
	ser.write(x[i]);
	sys.stderr.write("  " + str(1 + i) + "/" + str(len(x)) + "\r")
ser.close()

sys.stderr.write("\n")
