#!/usr/bin/env python3

import sys
sys.dont_write_bytecode = True
import os
import time
import subprocess

import config


class Item:


	def init(self,config,numero):
		self.cfg = config
		self.numero = numero


	def tick(self):
		print("No.: " + str(self.numero))



class Indicator:


	def main(self):

		self.loadConfig()
		self.run()


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

		self.slots = ["000"] * (1 + maxSlot)


	def run(self):

		while True:
			for item in self.items: item.tick()
			for slot in self.slots: print(slot,end=".")
			print()
			time.sleep(1)


if __name__ == '__main__':
	app = Indicator()
	try: app.main()
	except KeyboardInterrupt:
		print("\r - aborted")
		os._exit(0)
