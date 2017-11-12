#!/usr/bin/env python

import urllib2
import json
import time,datetime
import os
import ConfigParser

config=ConfigParser.ConfigParser()
config.read('/home/pertneer/Desktop/sunrise.ini')

localtime = time.localtime()
if(localtime.tm_isdst == 1):
        timeoffset = 5
else:
        timeoffset = 6

Lat = config.get('Location','Lat')
Lng = config.get('Location','Lng')

dateString = '%Y/%m/%d %H:%M:%S'
url="http://api.sunrise-sunset.org/json?lat=" + Lat + "&lng=" + Lng +"&formatted=0"
response=urllib2.urlopen(url)
data=json.load(response)

#print data
results=data['results']
fullSunrise=results['sunrise']
fullSunset=results['sunset']

#print ""
#print fullSunrise
#print""
#print fullSunset
#print""
sunRiseDate,sunRiseTime=fullSunrise.split("T")
sunRiseTime = sunRiseTime.split("+")
sunSetDate,sunSetTime=fullSunset.split("T")
sunSetTime=sunSetTime.split("+")
#print sunRiseTime[0]
#print""
#print sunSetTime[0]
#print""

sunsetHour,sunsetMinute,sunsetSecond=sunSetTime[0].split(":")
sunriseHour,sunriseMinute,sunsetSecond=sunRiseTime[0].split(":")
sunsetHour = int(sunsetHour)-timeoffset
sunriseHour = int(sunriseHour)-timeoffset

sunsetMinute = int(sunsetMinute)+int(config.get('Offsets','Sunset'))

if int(sunsetMinute) > 60:
	sunsetHour = int(sunsetHour) + 1
	sunsetMinute = int(sunsetMinute) - 60


cmd = 'sudo crontab -l | grep -v "python ' + config.get('FileLocations','chickenPy') + '" | sudo crontab -'
os.system(cmd)

time.sleep(5)

cmd = '(sudo crontab -l; echo " ' + str(sunriseMinute) + " " + str(sunriseHour) + ' * * * python /home/pertneer/Desktop/chicken.py") | sort - | uniq - | sudo crontab -'
os.system(cmd)

with open(config.get('FileLocations','logsunrise'),'a') as f:
	f.write(datetime.datetime.now().strftime(dateString) + "\n" + cmd + "\n")
	f.close()

cmd = '(sudo crontab -l; echo " ' + str(sunsetMinute) + " " + str(sunsetHour) + ' * * * python /home/pertneer/Desktop/chicken.py") | sort - | uniq - | sudo crontab -'
os.system(cmd)

with open(config.get('FileLocations','logsunset') ,'a') as f:
	f.write(datetime.datetime.now().strftime(dateString) + "\n" + cmd + "\n")
	f.close()

with open(config.get('FileLocations','sunriseConf') ,'r+') as f:
	f.seek(0)
	f.write(str(sunriseHour) + ":" + str(sunriseMinute))
	f.write('\n')
	f.write(str(sunsetHour) + ":" + str(sunsetMinute))
	f.close()

with open(config.get('FileLocations','log') ,'a') as f:
	f.write(datetime.datetime.now().strftime(dateString) + " sunrise.py\n")
	f.close()
