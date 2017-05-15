#!/usr/bin/env python3
import serial
import time
import sys

dev = "/dev/tty.wchusbserial1410"

ser = serial.Serial(
	dev,9600,
	timeout=2
)

crlf = False
while True:
	try:
		ser = serial.Serial(dev,9600,timeout=2)
	except:
		sys.stderr.write(".")
		crlf = True
		time.sleep(0.5)
		continue
	break
if crlf: sys.stderr.write("\n")

time.sleep(2)
w = 0.5

ser.write(bytes(b"+0:aff;"))
time.sleep(w)
ser.write(bytes(b"+2:f0f;"))
time.sleep(w)

ser.write(bytes(b"!"))

