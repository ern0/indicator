#!/usr/bin/env python3

import sys
sys.dont_write_bytecode = True
import os
import time
import serial
from importmodule import importmodule
from threading import Thread
from threading import Lock

#----------------------------------------------------------------------

class Indicator:


	def main(self):

		self.about()
		self.loadConfig()

		self.initLoadConfigFlags()
		self.initCheckEmptyConfig()
		self.initDevice()

		self.initShow()
		self.initForward()
		self.initCheck()
		self.initListen()

		while True: time.sleep(2018)


	def about(self):
		print("indicator")


	def noti(self,msg):
		print(" " + msg)


	def fatal(self,msg):
		self.noti("ERROR: " + msg)
		os._exit(1)


	def loadConfig(self):

		try:
			self.configName = sys.argv[1]
		except IndexError:
			self.fatal("config file not specified")

		try: 
			self.config = importmodule(self.configName)
		except FileNotFoundError:
			self.fatal("config not found: " + self.configName)
		except:
			type, value, traceback = sys.exc_info()
			self.fatal("invalid config: " + str(value))


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
		

	def send(self,data):

		if not self.showFlag: return
		self.serial.write(data.encode())


	def initShow(self):

		if not self.showFlag: return

		self.showLock = Lock()
		self.showData = {}

		self.show = Show(self)


	def initForward(self):

		if not self.forwardFlag: return

		self.forwardLock = Lock()
		self.forwardData = {}

		# todo


	def initCheck(self):

		if not self.checkFlag: return
		(Check(self)).start()



	def initListen(self):

		if not self.listenFlag: return

		# todo


	def registerResult(self,token,value):

		if self.forwardFlag:
			self.forwardLock.acquire()
			self.forwardData[token] = value
			self.forwardLock.release()

		if self.showFlag:
			self.showLock.acquire()
			self.showData[token] = value
			self.showLock.release()

#----------------------------------------------------------------------

class Check(Thread):


	def __init__(self,indicator):
		Thread.__init__(self)

		self.indicator = indicator
		self.initItems()


	def initItems(self):

		self.items = {}
		numero = 1

		for configItem in self.indicator.config.check:
			
			configItem["numero"] = numero
			self.items[numero] = CheckItem(configItem)

			try: 
				parm = configItem["parm"]
			except KeyError: 
				parm = None
				
			self.items[numero].module = configItem["module"]()

			try:
				self.items[numero].module.init(parm)
			except TypeError:
				self.items[numero].module.init()

			numero += 1


	def run(self):

		while True:

			for key in self.items:
				item = self.items[key]
				item.tick()
				if item.result is not None:
					self.indicator.registerResult(item.config["token"],item.result)

			if self.indicator.showFlag:
				self.indicator.show.update()

			time.sleep(1)

#----------------------------------------------------------------------

class CheckItem:

	def __init__(self,config):

		self.config = config

		try: self.counter = self.config["phase"]
		except KeyError: self.counter = 0


	def tick(self):

		self.result = None

		if self.config["freq"] <= 0: return

		if self.counter == 0: 
			
			try: 
				parm = self.config["parm"]
			except KeyError: 
				parm = None

			try:
				self.module.check(parm)
			except TypeError:
				self.module.check()
			self.result = self.module.getResult()

		self.counter += 1
		if self.counter >= self.config["freq"]: 
			self.counter = 0

#----------------------------------------------------------------------

class Module:	


	def setResult(self,value):
		self.result = value


	def getResult(self):
		return self.result


#----------------------------------------------------------------------

class Show():

	def __init__(self,indicator):
		
		self.indicator = indicator
		self.initSlots()

		time.sleep(2)
		self.indicator.send("!")


	def initSlots(self):
		
		config = self.indicator.config.show

		maxSlot = -1

		for showItem in config:
			slot = showItem["slot"]
			if slot > maxSlot: maxSlot = slot
		maxSlot += 1

		self.slots = ["000"] * (maxSlot)


	def update(self):

		self.fillSlots()
		self.composeResult()

		self.indicator.send(self.result)


	def fillSlots(self):

		config = self.indicator.config.show
		data = self.copyData()

		for showItem in config:
			slot = showItem["slot"]
			token = showItem["token"]
			colors = showItem["colors"]

			try: value = data[token]
			except KeyError: continue

			try: 
				color = colors[value]
			except KeyError: 
				color = colors[len(colors) - 1]

			self.slots[slot] = color


	def copyData(self):

		data = {}
		self.indicator.showLock.acquire()
		for i in self.indicator.showData: 
			data[i] = self.indicator.showData[i]
		self.indicator.showLock.release()

		return data


	def composeResult(self):

		self.result = ""
		for color in self.slots:

			if self.result == "": self.result = ":"
			else: self.result += "-"

			self.result += str(color)

		self.result += ";"


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
