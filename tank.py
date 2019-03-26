#! /usr/bin/python3

import ta7291p

class Tank():
	def __init__(self):
		self.left = ta7291p.TankMotor(5,6,12)
		self.right = ta7291p.TankMotor(19,26,13)
		self.speed = 50
		self.setspeed(self.speed)
		return
	def setspeed(self, myspeed):
		self.left.setspeed(myspeed)
		self.right.setspeed(myspeed)
		self.speed = myspeed
		return
	def leftturn(self):
		self.left.accelon(back=True)
		self.right.accelon()
		return
	def rightturn(self):
		self.left.accelon()
		self.right.accelon(back=True)
		return
	def forward(self):
		self.left.accelon()
		self.right.accelon()
		return
	def back(self):
		self.left.accelon(back=True)
		self.right.accelon(back=True)
		return
	def brake(self):
		self.left.brakeon()
		self.right.brakeon()
		return
	def acceloff(self):
		self.left.acceloff()
		self.right.acceloff()
		return

