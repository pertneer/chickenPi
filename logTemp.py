#!/usr/bin/env python
import time
import MySQLdb
time.sleep(10)
import urllib2
import datetime
import Adafruit_DHT
import RPi.GPIO as GPIO
import ConfigParser
config=ConfigParser.ConfigParser()
config.read('/home/pertneer/Desktop/config.ini')

dbHost = config.get('database','host')
dbUser = config.get('database','user')
dbPasswd = config.get('database','passwd')
dbDb = config.get('database','db')

db = MySQLdb.connect(host=dbHost,
                     user=dbUser,
                     passwd=dbPasswd,
                     db=dbDb)

cur = db.cursor()


outsidePin = int(config.get('DHT','outsidePin'))
insidePin = int(config.get('DHT','insidePin'))
doorOpenPin=int(config.get('Pins','doorOpenPin'))
doorClosePin=int(config.get('Pins','doorClosePin'))
sensor = Adafruit_DHT.DHT22
sleepTime = 15*60
dateString = '%Y/%m/%d %H:%M:%S'
sunRise = ""
sunSet = ""

def setup():
    global sunRise
    global sunSet
    if (GPIO.getmode() == 10) or (GPIO.getmode() == None):
	GPIO.setmode(GPIO.BCM)
    GPIO.setup(doorOpenPin, GPIO.IN, GPIO.PUD_UP)
    GPIO.setup(doorClosePin, GPIO.IN, GPIO.PUD_UP)

    humidity, temperature = Adafruit_DHT.read_retry(sensor, insidePin)
    humidityOut, temperatureOut = Adafruit_DHT.read_retry(sensor, outsidePin)


    if humidity is None and temperature is None:
            print 'Failed to get a reading. Please try again!'

    with open('/home/pertneer/Desktop/sunrise.conf','r') as s:
        sunTimes = s.readlines()
        s.close()
    
    sunRise = sunTimes[0].strip('\n').replace(':',".")
    sunSet = sunTimes[1].strip('\n').replace(':',".")
    
def writelog(message,location):
    with open("/home/pertneer/Desktop/%s" % location,'a') as f:
        f.write("{0} {1}\n".format(time.asctime( time.localtime(time.time())), message))

def loop():
    global sleepTime
    global sunRise
    global sunSet
    global sensor
    global pin
    
    log=True
    while log:
        db = MySQLdb.connect(host=dbHost,
                     user=dbUser,
                     passwd=dbPasswd,
                     db=dbDb)

        cur = db.cursor()
        if(GPIO.input(doorOpenPin) == 0):
            doorLoc = 1
            doorPosition='Open'
        elif(GPIO.input(doorClosePin) == 0):
            doorLoc = 0
            doorPosition='Close'
        else:
            doorLoc = .5
        humidity, temperature = Adafruit_DHT.read_retry(sensor, insidePin)
        humidityOut, temperatureOut = Adafruit_DHT.read_retry(sensor, outsidePin)
        temperature = temperature * 9/5 + 32
        temperature = "{:2.2f}".format(temperature)
        humidity = "{:2.2f}".format(humidity)
        temperatureOut = temperatureOut * 9/5 + 32
        temperatureOut = "{:2.2f}".format(temperatureOut)
        humidityOut = "{:2.2f}".format(humidityOut)
        currentTime = time.strftime(dateString)
        sqlQuery="INSERT INTO temperature(tempIn,tempOut,humidityIn,humidityOut,doorPosition,openTime,closeTime) VALUES (" + str(temperature) + ", " + str(temperatureOut) + ", " + str(humidity) + ", " + str(humidityOut) + ", '" + doorPosition + "', '" + sunRise + "', '" + sunSet + "')"
        if(temperatureOut < 120 and humidityOut < 100):
            cur.execute(sqlQuery)
            db.commit()
            db.close()
        else:
            logData = str(temperature) + "," + str(humidity) + "," + str(temperatureOut) + "," + str(humidityOut)
            writelog(logData,'Logs/tempData.csv')
        #time.sleep(sleepTime)
        log = False
        
def destroy():
    writelog('Destroy', 'log.csv')
    GPIO.cleanup() # Release resource
    db.close()

if __name__ == '__main__': # Program start from here
    setup()
    try:
        loop()
    except KeyboardInterrupt: # When 'Ctrl+C' is pressed, the child program destroy() will be executed.
        destroy()
