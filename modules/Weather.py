###################################################
# FILE: Weather.py                                #
# AUTHOR: NotPike                                 #
# Function: OWM API caller, voice to read weather #
#           https://openweathermap.org/           #
###################################################

import pyowm
import math
import logging

## Move back to root directory
import sys
sys.path.append("..")

from env import *
from utils.TX import *
from utils.Voice import *
from utils.Callsign import *

class Weather:

    env = ENV()
    voice = Voice()

    def __init__(self, 
                 call=env.CALLSIGN, 
                 api=env.OWM_API, 
                 gpio=env.GPIO, 
                 online=env.OWM_ONLINE):

        self.call = Callsign(call)
        self.tx = TX(gpio)
        self.apiKey = api
        self.online = online

    def readWeather(self, location='reno,usa'):
        try:
            owm = pyowm.OWM(self.apiKey)
            observation = owm.weather_at_place(location)
            w = observation.get_weather()
            self.online = True
        except:
            logging.warning("Weather Offline")
            self.online = False

            self.voice.buildAudio("Sorry. The weather is Offline")
            self.tx.txOn()
            self.voice.playAudio()
            self.call.cw()
            self.tx.txOff()

        if(self.online):
            temp = round(((w.get_temperature()['temp'] - 275.15) * (9/5) + 32), 1) # K -> F
            rh = w.get_humidity()
            windSpeed = round((w.get_wind()['speed'] * 2.237), 1)                  # MPS -> MPH
            windDirection = w.get_wind()['deg'] 

            report = "Air temperature, " + str(temp) + ". " + "Relative Humidity, " + str(rh) + ". " + "Wind Speed, " + str(windSpeed) + " Miles Per Hour. At " + str(windDirection) + " degrees."
            logging.info("Weather: " + report)

            self.voice.buildAudio(report)
            self.tx.txOn()
            self.voice.playAudio()
            self.call.cw()
            self.tx.txOff()
        else:
            return
