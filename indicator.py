#!/usr/bin/env python3

import sys
sys.dont_write_bytecode = True
import os
import time
import serial

import config


class Module:


	def init(self,numero,config):

		self.numero = numero
		self.config = config
		self.result = 0

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

		color = self.config["colors"][self.result]
		return color


class Indicator:


	def main(self):

		self.connect()
		self.loadConfig()
		self.run()


	def connect(self):

		dev = os.popen(
			"./detectdevice.sh"
		).read().split("\n")[0]

		if dev == "":
			print("no device found")
			os._exit(1)		

		self.serial = serial.Serial(dev,9600)
		time.sleep(1.5)
		self.send("!") # reset


	def send(self,data):
		self.serial.write(data.encode())


	def loadConfig(self):

		maxSlot = 0
		self.items = []
		numero = 1

		for configItem in config.cfg:

			item = configItem["module"]()
			del configItem["module"]
			item.init(numero,configItem)
			self.items.append(item)

			if item.config["slot"] > maxSlot:
				maxSlot = item.config["slot"]

			numero += 1

		self.slots = [None] * (1 + maxSlot)


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
			self.result += item.color()
		
		self.result += ";"


	def showResult(self):

		self.send(self.result)



if __name__ == '__main__':

	app = Indicator()
	try: app.main()
	except KeyboardInterrupt:
		app.send("!")
	except serial.serialutil.SerialException:
		type, value, traceback = sys.exc_info()
		print(value.args[0])
	os._exit(0)
