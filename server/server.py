#!/usr/bin/env python3

import sys
sys.dont_write_bytecode = True

import os
import time
import http.server
import socket
import socketserver
import urllib
import threading
import queue
from subprocess import Popen,PIPE

import config
import macros

if not config.test_disable_light:
	import serial
if not config.test_disable_sound:
	import pygame


class Server():
	
	def __init__(self):
		
		threading.Thread.__init__(self)	
		self.api = MacroApi()
		self.timer = Timer()
		self.timer.api = self.api


	def fatal(self,msg):
		print(msg)
		sys.exit(2)


	def changedir(self):

		try:
			os.chdir(config.webroot)
		except:
			self.api.log("invalid webroot: " + config.webroot,"startup")


	def discover(self,hints,signature):

		self.api.log("scanning for device, signature=\"" + signature + "\"","startup")

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

			self.api.log("found device=/dev/" + fnam,"startup")
			return ser

		self.api.log("not found","startup")
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
					self.api.log("waiting for port reuse","startup")
					warned = True
				time.sleep(0.5)
				continue

		self.api.initAudio()
		self.api.start()

		self.timer.start()

		self.httpd.theServer = self
		self.api.log("webserver started, port=" + str(config.port) + ", root=" + os.getcwd(),"startup")
		self.httpd.serve_forever()


	def main(self):

		self.changedir()

		if config.test_disable_light:
			self.api.log("lights are disabled","startup")
		else:
			ser = self.discover(config.light,"lite")
			if ser is None: return
			self.api.serial = ser

		self.startServer()


	def cleanup(self):
		try: self.httpd.server_close()
		except: pass
		

class ServerRequestHandler(http.server.SimpleHTTPRequestHandler):


	def log_message(self,format,*args):
		pass


	def send(self,txt):
		self.wfile.write(bytes(txt,"utf8"))


	def do_GET(self):

		sp = str(self.path + "///").split("/")
		if sp[1] == "light": 
			self.procMacro(sp[2],sp[3])
		elif sp[1] == "clock":
			self.procClock(sp[2],sp[3])
		else:
			http.server.SimpleHTTPRequestHandler.do_GET(self)


	def procMacro(self,macro,parm):

		self.send_response(200)
		self.send_header("Content-type","text/html; charset=utf-8")
		self.end_headers()

		self.send("macro enqueued \n")
		self.server.theServer.api.queue.put([macro,parm])


	def procClock(self,h,m):

		self.send_response(200)
		self.send_header("Content-type","text/html; charset=utf-8")
		self.end_headers()

		if h != "": 
			result = self.server.theServer.timer.set(h,m)
		else:
			result = self.server.theServer.timer.get()

		self.send(result)


class Timer(threading.Thread):

	def __init__(self):
		threading.Thread.__init__(self)

		self.hour = config.start_hour
		self.min = config.start_min
		self.running = False

		self.clockLock = threading.Lock()


	def log(self,msg):
		if not config.test_logging: return
		print("(timer) " + msg)


	def mkReply(self,h,m):
		return str(h) + "/" + str(m) + "/\n"


	def set(self,h,m):

		self.running = True

		h = int(h)
		m = int(m)

		self.clockLock.acquire()
		self.hour = h
		self.min = m
		self.clockLock.release()

		self.log("time set, stamp=" + self.getStamp())

		return self.mkReply(h,m)


	def get(self):

		self.running = True

		self.clockLock.acquire()
		h = self.hour
		m = self.min
		self.clockLock.release()

		return self.mkReply(h,m)


	def getStamp(self):

		h = str(self.hour)
		if self.hour < 10: h = "0" + h
		m = str(self.min)
		if self.min < 10: m = "0" + m

		return h + ":" + m


	def run(self):

		for i in range(1,4):
			if self.running: break
			time.sleep(1)
		if not self.running: 
			self.log("waiting for first client")
		while not self.running: 
			time.sleep(1)
		self.log("started, stamp=" + self.getStamp() + ", minute=" + str(config.minute))

		while True:
			time.sleep(config.minute)

			self.clockLock.acquire()

			self.api.queue.put(["clock",self.getStamp()])

			self.min += 1
			if self.min == 60:
				self.min = 0
				self.hour += 1
				if self.hour == 24: self.hour = 0

			self.clockLock.release()


class MacroApi(threading.Thread):

	def __init__(self):
		threading.Thread.__init__(self)
		self.initQueue()
		self.macros = macros.Macros()
		self.macros.api = self


	def log(self,msg,sig = None):
				
		if sig == None:
			if config.test_logging:
				b = "["
				e = "] "
				if self.parm == "": p = ""
				else: p = self.parm + " "
				sig = self.token
			else:
				return
		else:
			p = ""
			if config.test_logging:
				b = "("
				e = ") "	
			else:
				b = ""
				e = ""
				sig = ""
		
		print(b + sig + e  + p + msg)
		

	def initQueue(self):
		self.queue = queue.Queue()
		self.queue.put(["init"])


	def initAudio(self):

		if config.test_disable_sound:
			self.log("audio is disabled","startup")
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

		self.log("audio ok, files=" + str(num),"startup")


	def run(self):

		while True:

			q = self.queue.get()
			self.token = q[0]
			try: self.parm = q[1]
			except: self.parm = ""

			try:
				macroFunction = getattr(self.macros,self.token)
			except:
				self.log("error: missing macro: " + self.token,"commproc")
				continue

			try:
				self.cmd = ""
				self.log(">>>> begin")
				if self.parm == "": result = macroFunction()
				else: result = macroFunction(self.parm)
			except:
				self.log("<<<< error: " + str(sys.exc_info()))
				self.cmd = ""
				continue

			if self.cmd != "": self.send()
			self.log("<<<< end")


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
		self.log("light: " + cmd)
		if not config.test_disable_light:
			self.serial.write(bytes(cmd,"utf-8"))
		self.cmd = ""
		time.sleep(0.1)


	def sleep(self,sec):
		self.send()
		time.sleep(sec)


	def findSound(self,pattern):
	
		if config.test_disable_sound: 
			self.log("sound: " + pattern + " (disabled)")			
			return None
		
		for name in self.sounds:
			if not pattern in name: continue
			self.log("sound: " + pattern)			
			return self.sounds[name]

		self.log("no sound file found: " + pattern)
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
		print("\r(cleanup) aborted")
		os._exit(0)
