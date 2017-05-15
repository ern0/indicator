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


import config


class Server():
	
	def __init__(self):
		
		threading.Thread.__init__(self)
		self.light = LightProc()


	def fatal(self,msg):
		print(msg)
		sys.exit(2)


	def main(self):

		httpd = socketserver.TCPServer(
			("",config.port),
			ServerRequestHandler
		)
		httpd.socket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
		httpd.theServer = self
		print("server started, port=" + str(config.port))
		httpd.serve_forever()


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
			item = self.queue.get()
			print(item)


if __name__ == '__main__':
	(Server()).main()
