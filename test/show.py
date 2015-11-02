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

x = "262"
x += "383"
x += "4B4"
x += "273"
x += "395"
x += "5B6"
x += "374"
x += "496"
x += "5B7"
x += "376"
x += "4A7"
x += "5B9"
x += "387"
x += "4A9"
x += "5BA"
x += "388"
x += "4AA"
x += "6BC"
x += "378"
x += "49B"
x += "6AC"
x += "369"
x += "48B"
x += "69C"
x += "359"
x += "47B"
x += "68C"
x += "34A"
x += "45C"
x += "77C"
x += "43A"
x += "55C"
x += "77D"
x += "53A"
x += "75C"
x += "97D"
x += "73B"
x += "85C"
x += "A7D"
x += "93B"
x += "A5C"
x += "B8D"
x += "B3B"
x += "C6C"
x += "D8D"
x += "C3B"
x += "D6C"
x += "D8D"
x += "C49"
x += "D6B"
x += "D9C"
x += "C48"
x += "D6A"
x += "E9B"
x += "C46"
x += "D78"
x += "E9A"
x += "C55"
x += "D77"
x += "EAA"
x += "D65"
x += "D87"
x += "EAA"
x += "D85"
x += "DA8"
x += "ECA"
x += "DA5"
x += "EB8"
x += "EDA"
x += "DB6"
x += "EC8"
x += "EDB"
x += "DD6"
x += "EE9"
x += "EEB"
x += "CD6"
x += "DE9"
x += "EFB"
x += "BD7"
x += "CE9"
x += "EFC"
x += "AE7"
x += "BEA"
x += "DFC"
x += "9E7"
x += "BEA"
x += "DFC"
x += "8E8"
x += "AEA"
x += "DFD"

ser.write("*30")

start = 0
while True:
	ser.write(":")
	pos = start
	for i in range(1,3 * 16):
		ser.write(x[pos])
		pos += 1
		ser.write(x[pos])
		pos += 1
		ser.write(x[pos])
		pos += 1
		if pos >= len(x): pos = 0
	ser.write(";");
	start += 3
	if start >= len(x): start = 0
