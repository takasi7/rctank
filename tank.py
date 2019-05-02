#! /usr/bin/python3
import os
import signal
import ta7291p

SENSORPATH='/home/pi/TA7291P/gp2y.py'
class Tank():
	def __init__(self):
		self.left = ta7291p.TankMotor(5,6,12)
		self.right = ta7291p.TankMotor(19,26,13)
		self.speed = 50
		self.state = 0
		self.setspeed(self.speed)
		self.pid = 0
		return
	def killsafty(self):
		if self.pid != 0:
			os.kill(self.pid,signal.SIGKILL)
		self.pid = 0
		return
	def safty(self):
		#return
		self.killsafty()
		self.pid = os.fork()
		if self.pid == 0:
			os.execl(SENSORPATH,SENSORPATH,str(self.state),str(self.speed))
		return
	def setspeed(self, myspeed):
		self.left.setspeed(myspeed)
		self.right.setspeed(myspeed)
		self.speed = myspeed
		return
	def leftturn(self,nosafty=False):
		self.left.accelon(back=True)
		self.right.accelon()
		if nosafty == False:
			self.state = 5
			self.safty()
		return
	def rightturn(self,nosafty=False):
		self.left.accelon()
		self.right.accelon(back=True)
		if nosafty == False:
			self.state = 3
			self.safty()
		return
	def forward(self,nosafty=False):
		self.left.accelon()
		self.right.accelon()
		if nosafty == False:
			self.state = 2
			self.safty()
		return
	def back(self,nosafty=False):
		self.left.accelon(back=True)
		self.right.accelon(back=True)
		if nosafty == False:
			self.state = 4
			#self.safty()
			self.killsafty()
		return
	def brake(self,nosafty=False):
		self.left.brakeon()
		self.right.brakeon()
		if nosafty == False:
			self.state = 0
			self.killsafty()
		return
	def acceloff(self,nosafty=False):
		self.left.acceloff()
		self.right.acceloff()
		if nosafty == False:
			self.state = 1
			self.killsafty()
		return

