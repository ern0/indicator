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

		self.initLoadConfigFlags()
		self.initCheckEmptyConfig()
		self.initDevice()
		self.resetDevice()

		self.initShow()
		self.initForward()
		self.initCheck()
		self.initListen()

		while True:
			sys.stderr.write(".")
			sys.stderr.flush()
			time.sleep(4)


	def about(self):
		print("indicator")


	def noti(self,msg):
		print(" " + msg)


	def fatal(self,msg):
		self.noti("ERROR: " + msg)
		os._exit(1)


	def loadConfig(self):

		self.configName = sys.argv[1]
		try: 
			self.config = __import__(self.configName.replace(".py",""))
		except ModuleNotFoundError:
			self.fatal("config not found: " + self.configName)


	def initLoadConfigFlags(self):

		try: 
			dummy = self.config.check
			self.checkFlag = True
		except AttributeError:
			self.checkFlag = False

		try: 
			dummy = self.config.show
			self.showFlag = True
		except AttributeError:
			self.showFlag = False

		try: 
			dummy = self.config.listen
			self.listenFlag = True
		except AttributeError:
			self.listenFlag = False

		try: 
			dummy = self.config.forward
			self.forwardFlag = True
		except AttributeError:
			self.forwardFlag = False

		try: 
			dummy = self.config.device
			self.forcedDeviceFlag = True
		except AttributeError:
			self.forcedDeviceFlag = False


	def initCheckEmptyConfig(self):

		isAnySource = self.checkFlag or self.listenFlag
		isAnySink = self.showFlag or self.forwardFlag

		if not (isAnySource or isAnySink):
			self.fatal("configuration is empty: " + self.configName)
		self.noti("configuration: " + self.configName)

		if not isAnySource:
			self.fatal("no input configured")

		if not isAnySink:
			self.fatal("no output configured")


	def initDevice(self):

		if not self.showFlag: return

		self.openDevice()

		if self.device is None:
			if self.forcedDeviceFlag: 
				self.fatal("device not found: " + self.config.device)
			else: 
				self.fatal("no device found")
			return

		self.noti("device found: " + self.device)

		self.serialLock = Lock()
		self.serialData = {}


	def openDevice(self):

		self.device = None

		try: 
			self.device = self.config.device
		except AttributeError:
			self.device = self.detectDevice()
		
		if self.device is None: return

		try:
			self.serial = serial.Serial(self.device,9600)
		except Exception:
			self.device = None
			return


	def detectDevice(self):
		
		devDir = os.listdir("/dev")
		for devFile in devDir:			
		
			if "Bluetooth" in devFile: continue
			
			found = False
			if devFile.find("tty.") == 0: found = True
			if devFile[0:6] == "ttyUSB": found = True
			if devFile[0:6] == "ttyACM": found = True
			
			if found: return "/dev/" + devFile
		
		return None
		

	def resetDevice(self):

		if not self.showFlag: return

		time.sleep(2)
		self.send("!")


	def send(self,data):

		if not self.showFlag: return
		self.serial.write(data.encode())


	def initShow(self):

		if not self.showFlag: return

		self.showLock = Lock()
		self.showData = {}

		print("todo... init show")


	def initForward(self):

		if not self.forwardFlag: return

		self.forwardLock = Lock()
		self.forwardData = {}

		print("todo... init forward")


	def initCheck(self):

		if not self.checkFlag: return

		print("todo... init check")


	def initListen(self):

		if not self.listenFlag: return

		print("todo... init listen")




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
