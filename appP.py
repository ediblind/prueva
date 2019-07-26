#!/usr/bin/python

try:
	from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
except:
	from http.server import BaseHTTPRequestHandler,HTTPServer
from os import curdir, sep
try:
	from urlparse import urlparse
	from urlparse import urlparse, parse_qs
except:
	from urllib.parse import urlparse, parse_qs
import RPi.GPIO as gpio

gpio.setmode(gpio.BOARD)
gpio.setup(3,gpio.OUT)
gpio.setup(5,gpio.OUT)

gpio.output(3,False)
gpio.output(5,False)

import os
port = int(os.environ.get("PORT", 5001))	
PORT_NUMBER = port

sensor=0
#This class will handles any incoming request from
#the browser

def ledS(path):
		global l1
		global l2
		print path.split('_')
		try:
				cmd,v=path.split('_')
		except:
				cmd=''
		if cmd=='/led1':
				if l1=='1':
						gpio.output(3,True)
						print "led1 on"
				if l1=='0':
						gpio.output(3,False)
						print "led1 off"
		if cmd=='/led2':
				if l2=='1':
						gpio.output(5,True)
						print "led2 on"
				if l2=='0':
						gpio.output(5,False)
						print "led2 off"

class myHandler(BaseHTTPRequestHandler):
	
	#Handler for the GET requests
	def do_GET(self):
		global s1,s2,s3
                print 'my path es: '+self.path
                ledS(self.path)
                self.path='/'
		if self.path=="/":  #127.0.0.1:5000/
			self.path="/index.html" #127.0.0.1:5000/index.html

		try:
			#Check the file extension required and
			#set the right mime type

			sendReply = False
			if self.path.endswith(".html"):
				mimetype='text/html'
				sendReply = True
			if self.path.endswith(".jpg"):
				mimetype='image/jpg'
				sendReply = True
			if self.path.endswith(".gif"):
				mimetype='image/gif'
				sendReply = True
			if self.path.endswith(".js"):
				mimetype='application/javascript'
				sendReply = True
			if self.path.endswith(".css"):
				mimetype='text/css'
				sendReply = True

			if sendReply == True:
				#Open the static file requested and send it
				f = open(curdir + sep + self.path) 
				self.send_response(200)
				self.send_header('Content-type',mimetype)
				self.end_headers()
				data=f.read()
				try:
					self.wfile.write(data)
				except:
					self.wfile.write(bytes(data, 'UTF-8'))
				f.close()
			return

		except IOError:
			self.send_error(404,'File Not Found: %s' % self.path)

try:
	#Create a web server and define the handler to manage the
	#incoming request
	server = HTTPServer(('0.0.0.0', PORT_NUMBER), myHandler)
	print ('Started httpserver on port ' , PORT_NUMBER)
	
	#Wait forever for incoming htto requests
	server.serve_forever()

except KeyboardInterrupt:
	print ('^C received, shutting down the web server')
	server.socket.close()
