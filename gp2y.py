#! /usr/bin/python3
# -*- coding: utf-8 -*-
import sys
import smbus
from tank import Tank
from time import sleep

bus=smbus.SMBus(1)
address_gpy2=0x40
register_gpyu=0x5E
register_gpys=0x5F
THRESHOLD = 12.0
BACKTIME=1.0
OUTLIER=58.0

def read_gpy2():
	data=0
	#11-4bit data
	ue=bus.read_word_data(address_gpy2,register_gpyu)
	#3-0bit data
	shita=bus.read_word_data(address_gpy2,register_gpys)
	ue=ue & 0xff
	shita=shita & 0xff
	data =((ue*16+shita)/16)/4
	return data

def restore():
	ct = 0
	while True:
		inputValue = read_gpy2()
		if inputValue < THRESHOLD:
			break
		sleep(0.5)
		ct += 1
		if ct > 20:
			break
	return

def emergency(state,speed=50):
	tk = Tank()
	tk.setspeed(speed)
	tk.brake(True)
	if state == 2:
		tk.back(True)
		restore()
	elif state == 4:
		tk.forward(True)
		restore()
	elif state == 3:
		tk.leftturn(True)
		restore()
	elif state == 5:
		tk.rightturn(True)
		restore()
	tk.brake()
	return


state = int(sys.argv[1])
speed = int(sys.argv[2])
fOutlier=False
while True:
	inputValue = read_gpy2()
	#print(inputValue)
	if inputValue > OUTLIER and fOutlier == False:
		sleep(0.1)
		fOutlier = True
		continue
	elif inputValue > THRESHOLD:
		emergency(state,speed)
		break
	fOutlier = False
	sleep(0.5)

