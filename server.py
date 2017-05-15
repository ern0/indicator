#!/usr/bin/env python3

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
import serial


import config


class Server():
	
	def __init__(self):
		
		threading.Thread.__init__(self)
		self.light = LightProc()


	def fatal(self,msg):
		print(msg)
		sys.exit(2)


	def discover(self,hints,signature):

		print("discovery: " + signature)

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

			print("found /dev/" + fnam)
			return ser

		print("not found")
		return None


	def startServer(self):

		httpd = socketserver.TCPServer(
			("",config.port),
			ServerRequestHandler
		)
		httpd.socket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
		httpd.theServer = self
		print("webserver started, port=" + str(config.port))
		httpd.serve_forever()


	def main(self):

		ser = self.discover(config.ligth,"lite")
		if ser is None: return
		self.light.seral = ser

		self.startServer()


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

		self.send("light enqueued \n")
		self.server.theServer.light.queue.put(macro)


class LightProc(threading.Thread):


	def __init__(self):

		threading.Thread.__init__(self);
		self.queue = queue.Queue()
		self.start()


	def run(self):

		while True:

			macro = self.queue.get()
			try:
				cmd = config.macros[macro]
			except:
				print("invalid macro: " + macro)
				continue

			print(cmd)


if __name__ == '__main__':
	(Server()).main()
