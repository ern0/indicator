#!/usr/bin/env python3

import sys
sys.dont_write_bytecode = True
import os
import time
import serial
from threading import Thread
from threading import Lock


class Indicator:


	def main(self):

		self.about()
		self.loadConfig()

		self.initConcurrency()
		#self.connect()
		#self.run()


	def about(self):
		print("indicator")


	def noti(self,msg):
		print(" " + msg)


	def fatal(self,msg):
		self.noti(msg)
		os._exit(1)


	def loadConfig(self):

		configName = sys.argv[1]
		try: 
			self.config = __import__(configName.replace(".py",""))
		except ModuleNotFoundError:
			self.fatal("config not found:s " + configName)

		self.noti("configuration: " + configName)


	def initConcurrency(self):
		
		self.serialFlag = False
		self.serialLock = Lock()
		self.serialData = {}
		
		self.forwardFlag = False
		self.forwardLock = Lock()
		self.forwardData = {}
		

	def detectDevice(self):
		
		devDir = os.listdir("/dev")
		for devFile in devDir:			
		
			if "Bluetooth" in devFile: continue
			
			found = False
			if "dev." in devFile: found = True
			if devFile[0:6] == "ttyUSB": found = True
			if devFile[0:6] == "ttyACM": found = True
			
			if found: return "/dev/" + devFile
		
		return None
		

	def connect(self):

		dev = self.detectDevice()

		if dev is None:
			print("no device found")
			os._exit(1)		

		self.serial = serial.Serial(dev,9600)
		time.sleep(2)
		
		self.send("!") # reset


	def send(self,data):
		self.serial.write(data.encode())


	def run(self):

		while True:

			self.scanItems()
			self.collectSlots()
			self.showResult()
			time.sleep(1)


	def scanItems(self):

		for item in self.items: 
			active = item.tick()
			if active:
				slotIndex = item.config["slot"]
				self.slots[slotIndex] = item


	def collectSlots(self):

		self.result = ""

		for item in self.slots:
			
			if self.result == "": self.result = ":"
			else: self.result += "-"

			if item is None: self.result += "000"
			else: self.result += item.color()
		
		self.result += ";"


	def showResult(self):

		self.send(self.result)


class Module:

	def init(self,numero,config):

		self.numero = numero
		self.config = config
		self.result = 0
		self.last = "000"

		try: self.counter = self.config["phase"]
		except KeyError: self.counter = 0
		

	def tick(self):

		active = False

		if self.counter == 0: 
			chk = self.check()
			if chk is not None: 
				self.result = chk
				active = True

		self.counter += 1
		if self.counter >= self.config["freq"]: 
			self.counter = 0

		return active


	def color(self):

		if self.result is None:
			return self.last

		index = self.result
		if index >= len(self.config["colors"]):
			index = len(self.config["colors"]) - 1
		color = self.config["colors"][index]

		self.last = color

		return color


if __name__ == '__main__':

	app = Indicator()
	try: app.main()
	except KeyboardInterrupt:
		app.send("!")
	except PermissionError:
		print("need permission for serial port")
	except serial.serialutil.SerialException:
		type, value, traceback = sys.exc_info()
		print(value.args)
	os._exit(0)
