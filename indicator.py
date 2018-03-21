#!/usr/bin/env python3

import sys
sys.dont_write_bytecode = True
import os
import time
import serial

import config


class Item:


	def init(self,config,numero):

		self.cfg = config
		self.numero = numero

		try: self.counter = self.cfg["phase"]
		except KeyError: self.counter = 0

		self.result = False


	def tick(self):

		active = False

		if self.counter == 0: 
			self.result = self.check()
			active = True

		self.counter += 1
		if self.counter >= self.cfg["freq"]: 
			self.counter = 0

		return active


	def check(self):

		func = self.cfg["func"]
		try: parm = self.cfg["parm"]
		except KeyError: parm = None

		return func(parm)


	def color(self):

		if self.result: return "fff"
		else: return "000"


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

			item = Item()
			item.init(configItem,numero)
			self.items.append(item)

			if item.cfg["slot"] > maxSlot:
				maxSlot = item.cfg["slot"]

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
				slotIndex = item.cfg["slot"]
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
		print("\r - aborted")
		os._exit(0)
