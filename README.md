# chickenPi
Raspberry Pi controlled chicken coop door

# Setup!

  - git clone https://github.com/pertneer/chickenPi.git
  - edit config.ini to reflect your email settings
  - edit sunrise.ini
    - change Lat and Lng to your location
    - sunset offset moves time to after sunrise to allow chickens time to go into coop
    - edit file location for where each file is located

### Important

open command line and run following command
   - sudo python /home/\<Username\>/Desktop/sunrise.py
      - this will set initial time to open and close the door
   - sudo crontab -e
      - edit cron to add the following
         - 0 4 * * * python /home/\<Username\>/Desktop/sunrise.py
      - this will run the sunrise program each morning at 4 a.m. to get the days sunrise and sunset times
