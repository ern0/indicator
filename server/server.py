#!/usr/bin/env python3

import config
import macros

import sys
import os
import time
import http.server
import socket
import socketserver
import urllib
import threading
import queue
from subprocess import Popen,PIPE
if not config.test_disable_light:
	import serial
if not config.test_disable_sound:
	import pygame


class Server():
	
	def __init__(self):
		
		threading.Thread.__init__(self)
		self.api = MacroApi()


	def fatal(self,msg):
		print(msg)
		sys.exit(2)


	def changedir(self):

		try:
			os.chdir(config.webroot)
		except:
			self.fatal("invalid webroot: " + config.webroot)


	def discover(self,hints,signature):

		print("scanning for device, signature=\"" + signature + "\"")

		for fnam in os.listdir("/dev"):

			candidate = False
			for hint in hints:
				if fnam[0:len(hint)] == hint:
					candidate = True
					break
			if not candidate: continue

			try:
				ser = serial.Serial("/dev/" + fnam,9600,timeout=0.2)
			except:
				continue

			time.sleep(2)
			ser.write(b"?")
			time.sleep(0.1)
			reply = ser.read(99).decode("utf-8")
			if reply[0:len(signature)] != signature: continue

			print("found device=/dev/" + fnam)
			return ser

		print("not found")
		return None


	def startServer(self):

		warned = False
		while True:
			try:
				self.httpd = socketserver.TCPServer(
					("",config.port),
					ServerRequestHandler
				)
				break
			except OSError:
				if not warned: 
					print("waiting for port reuse")
					warned = True
				time.sleep(0.5)
				continue

		self.api.initAudio()
		self.api.start()

		self.httpd.theServer = self
		print("webserver started, port=" + str(config.port) + ", root=" + os.getcwd())
		self.httpd.serve_forever()


	def main(self):

		self.changedir()

		if config.test_disable_light:
			print("lights are disabled")
		else:
			ser = self.discover(config.light,"lite")
			if ser is None: return
			self.api.serial = ser

		self.startServer()


	def cleanup(self):
		self.httpd.server_close()
		

class ServerRequestHandler(http.server.SimpleHTTPRequestHandler):


	def log_message(self,format,*args):
		pass


	def send(self,txt):
		self.wfile.write(bytes(txt,"utf8"))


	def do_GET(self):

		sp = str(self.path).split("/")
		if sp[1] == "light": 
			self.procMacro(sp[2])
		else:
			http.server.SimpleHTTPRequestHandler.do_GET(self)


	def procMacro(self,macro):

		self.send_response(200)
		self.send_header("Content-type","text/html; charset=utf-8")
		self.end_headers()

		self.send("macro enqueued \n")
		self.server.theServer.api.queue.put(macro)


class MacroApi(threading.Thread):


	def __init__(self):
		threading.Thread.__init__(self);
		self.initQueue();
		self.macros = macros.Macros()
		self.macros.api = self


	def initQueue(self):
		self.queue = queue.Queue()
		self.queue.put("init")


	def initAudio(self):

		if config.test_disable_sound:
			print("audio is disabled")
			return
			
		self.sounds = {}
		pygame.mixer.init()

		if config.sound[0] == "/":
			sdir = config.sound
		else:
			sdir = "../" + config.sound

		num = 0
		for fnam in os.listdir(sdir):
			full = sdir + "/" + fnam
			self.sounds[fnam] = pygame.mixer.Sound(full)
			num += 1

		print("audio ok, files=" + str(num))


	def run(self):

		while True:

			self.token = self.queue.get()

			try:
				macroFunction = getattr(self.macros,self.token)
			except:
				print("[" + self.token + "] error: missing macro")
				continue

			try:
				self.cmd = ""
				result = macroFunction()
			except:
				print("[" + self.token + "] error: " + sys.exc_info())

			if self.cmd != "": self.send()


	def lum(self,value):
		self.cmd = self.cmd + "*" + str(value)


	def pos(self,value):
		self.cmd = self.cmd + "+" + str(value)


	def hex(self,colors):

		if not type(colors) is list:
			colors = [colors]

		self.cmd = self.cmd + ":"
		for color in colors:
			self.cmd = self.cmd + color


	def light(self,positions,value):
		
		if not type(positions) is list:
			positions = [positions]

		for position in positions:
			self.pos(position)
			self.hex(value)


	def reset(self):
		self.send("!")


	def send(self,cmd = None):

		if cmd is None: cmd = self.cmd + ";"
		if config.test_disable_light:
			print("[" + self.token + "] light: " + cmd);
		else:
			self.serial.write(bytes(cmd,"utf-8"))
		self.cmd = ""
		time.sleep(0.1)


	def sleep(self,sec):
		self.send()
		time.sleep(sec)


	def findSound(self,pattern):
		
		if config.test_disable_sound: 
			print("[" + self.token + "] sound: " + pattern);
			return None
		
		for name in self.sounds:
			if not pattern in name: continue
			return self.sounds[name]

		print("no sound file found: " + pattern)
		return None


	def bgplay(self,pattern,wait=False):

		self.send()
		sound = self.findSound(pattern)
		if sound is None: return

		sound.play()

		if not wait: return
		while pygame.mixer.get_busy(): time.sleep(0.1)


	def fgplay(self,pattern):
		self.bgplay(pattern,True)


if __name__ == '__main__':
	server = Server()
	try: server.main()
	except KeyboardInterrupt:
		server.cleanup()
		print("\rshutdown")
		os._exit(0)
