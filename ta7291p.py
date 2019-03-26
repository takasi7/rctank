#! /usr/bin/python3

import RPi.GPIO as GPIO

ST_STOP = 0
ST_ON = 1

class TankMotor :
	
	def __init__(self,pina,pinb,pwmpin):
		self.state = ST_STOP
		self.pina = pina
		self.pinb = pinb
		self.pwmpin = pwmpin
		self.duty = 0
		self.pulse = 1000

		GPIO.setmode(GPIO.BCM)
		
		GPIO.setup(self.pina, GPIO.OUT)
		GPIO.output(self.pina, GPIO.LOW)
		
		GPIO.setup(self.pinb, GPIO.OUT)
		GPIO.output(self.pinb, GPIO.LOW)
		
		GPIO.setup(self.pwmpin, GPIO.OUT)
		GPIO.output(self.pwmpin, GPIO.LOW)
		
		self.pwm = GPIO.PWM(self.pwmpin,1000)
		return

	def setspeed(self,duty):
		self.duty = duty
		if self.state == ST_ON:
			self.pwm.ChangeDutyCycle(self.duty)
		return self.state

	def accelon(self,back = False):
		if back == False:
			GPIO.output(self.pina, GPIO.HIGH)
			GPIO.output(self.pinb, GPIO.LOW)
		else:
			GPIO.output(self.pina, GPIO.LOW)
			GPIO.output(self.pinb, GPIO.HIGH)

		if self.state == ST_STOP:
			self.pwm.start(self.duty)

		self.state = ST_ON
		return self.state
	
	def acceloff(self):
		GPIO.output(self.pina, GPIO.LOW)
		GPIO.output(self.pinb, GPIO.LOW)
		self.pwm.stop()
		self.state = ST_STOP
		return self.state
	
	def brakeon(self):
		GPIO.output(self.pina, GPIO.HIGH)
		GPIO.output(self.pinb, GPIO.HIGH)
		self.pwm.stop()
		GPIO.output(self.pina, GPIO.LOW)
		GPIO.output(self.pinb, GPIO.LOW)
		self.state = ST_STOP
		return self.state

