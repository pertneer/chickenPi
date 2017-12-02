#!/usr/bin/env python

import RPi.GPIO as GPIO
import time,datetime
import ConfigParser
from smtplib import SMTP
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText

debug=False
message = "Debug"
body= "Debug Body"
dateString = '%Y/%m/%d %H:%M:%S'
currentDateString = '%H'
currentTime = time.strftime(currentDateString)

config=ConfigParser.ConfigParser()
config.read('/home/pertneer/Desktop/config.ini')

powerPin=int(config.get('Pins','powerPin'))
doorOpenPin=int(config.get('Pins','doorOpenPin'))
doorClosePin=int(config.get('Pins','doorClosePin'))
fromAddr=config.get('Email','fromAddr')
toAddr=config.get('Email','toAddr')
fromPasswrd=config.get('Email','fromPasswrd')
servAddr=config.get('Email','servAddr')

if (GPIO.getmode() == 10) or (GPIO.getmode() == None):
	GPIO.setmode(GPIO.BCM)

GPIO.setup(powerPin, GPIO.OUT)
GPIO.output(powerPin, False)
GPIO.setup(doorOpenPin, GPIO.IN, GPIO.PUD_UP)
GPIO.setup(doorClosePin, GPIO.IN, GPIO.PUD_UP)


def sendEmail(subject="Test",body="Message Body"):
    if (debug == False):
        addresses = toAddr.split(",")

        for address in addresses:
                server = SMTP(servAddr,587)
                server.set_debuglevel(True)
                server.starttls()
                server.login(fromAddr,fromPasswrd)

                server.sendmail(fromAddr, address, subject)
                time.sleep(.1)
                server.sendmail(fromAddr, address, body)
                server.quit()

        return True

    else:
        print "Message: " + body
        print "Subject: " + subject

count = 1
operating = True

if (GPIO.input(doorOpenPin) == 0):
    #Door is Open
        if(int(currentTime) > 12):
            GPIO.output(powerPin,True)
            print "door is closing"
            #print GPIO.input(doorClosePin)
            while operating:
                    if (GPIO.input(doorClosePin) == 0):
                        #door shut successfully
                        message = 'Door Shut was successful'
                        if(debug):
                                print message
                        body="Chickens are all locked in for the night!"
                        operating = False
                    elif(count > 5):
                        #door did not shut
                        message = 'Door Shut operation Failed'
                        if(debug):
                                print message
                        body="You need to check the door!"
                        operating = False
                    else:
                        time.sleep(10)
                        print str(count) + " closing operation"
                        count = count + 1
            GPIO.output(powerPin,False)
            print "Power is off to motor"
        else:
           print "Door is already open"
           message = "Door is already open"
           body = "Door Was triggered before 12 when door was already open"
elif (GPIO.input(doorClosePin) == 0):
    #Door Closed
    
        
        if(int(currentTime) > 12):
            print currentTime
            print "Door Is already closed"
            message = "Door was alread shut"
            body = "Door was trigger after 12 when door was already shut"
        else:
            GPIO.output(powerPin,True)
            print "door is opening"
            #print GPIO.input(doorClosePin)
            while operating:
                    if (GPIO.input(doorOpenPin) == 0):
                        #door shut successfully
                        message = 'Door Open was successful'
                        if(debug):
                                print message
                        body="Chickens are out to roam!"
                        operating = False
                    elif(count > 5):
                        #door did not shut
                        message = 'Door Open operation Failed'
                        if(debug):
                                print message
                        body="You need to check the door!"
                        operating = False
                    else:
                        time.sleep(10)
                        print str(count) + " opening operation"
                        count = count + 1
            GPIO.output(powerPin,False)
            print "Power is off to motor"
else:
    #error
    message = "Door Error"
    body = 'Door is not open or shut when initiating sequence'
    print "Error"


with open(config.get('FileLocations','log') ,'a') as f:
	f.write(datetime.datetime.now().strftime(dateString) + " chicken.py\n")
	f.close()

sendEmail(message,body)
GPIO.cleanup()
