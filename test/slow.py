#!/usr/bin/python2
import serial
import time
import sys

crlf = False
while True:
	try:
		ser = serial.Serial('/dev/ttyACM0',38400,timeout=2)
	except:
		sys.stderr.write(".")
		crlf = True
		time.sleep(0.5)
		continue
	break
if crlf: sys.stderr.write("\n")

x = ":ccf-404-404-111-40f-111-400-004-40f-400-004-400-400-004-400-fee;"

for i in range(0,len(x)):
	ser.write(x[i])
	sys.stderr.write("|")
	if i % 10 == 0: time.sleep(0.3)
ser.close()

sys.stderr.write("\n")
