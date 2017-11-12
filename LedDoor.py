#!/usr/bin/env python
debug=False
import time
import RPi.GPIO as GPIO
import ConfigParser

config=ConfigParser.ConfigParser()
config.read('/home/pertneer/Desktop/config.ini')

GPIO.setwarnings(False)
if (GPIO.getmode() == 10) or (GPIO.getmode() == None):
	GPIO.setmode(GPIO.BCM)

doorOpenPin=int(config.get('Pins','doorOpenPin'))
doorClosePin=int(config.get('Pins','doorClosePin'))
if(debug):
    print doorClosePin
    print doorOpenPin
greenPin=int(config.get('Led','greenPin'))
redPin=int(config.get('Led','redPin'))
if(debug):
    print redPin
    print greenPin
GPIO.setup(doorOpenPin, GPIO.IN, GPIO.PUD_UP)
GPIO.setup(doorClosePin, GPIO.IN, GPIO.PUD_UP)
GPIO.setup(greenPin,GPIO.OUT)
GPIO.setup(redPin,GPIO.OUT)

while True:
    if ((GPIO.input(doorOpenPin) == 0) or (GPIO.input(doorClosePin) == 0)):
        if(debug):
            print GPIO.input(doorOpenPin)
            print GPIO.input(doorClosePin)
        GPIO.output(greenPin, True)
        GPIO.output(redPin, False)
        time.sleep(3)
    else:
        if(debug):
            print GPIO.input(doorOpenPin)
            print GPIO.input(doorClosePin)
        GPIO.output(greenPin, False)
        GPIO.output(redPin, True)
        time.sleep(3)
        
GPIO.cleanup()
