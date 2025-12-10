import sys
import os

import RPi.GPIO as GPIO
import dht11
import time
import datetime

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "lib/tempsensor"))
import tempsensor_setup
import tempsensor

GPIO.setwarnings(True)
GPIO.setmode(GPIO.BCM)
PIN = 4 #Placeholder
instance = dht11.DHT11(PIN)

class TEMP_STAT : 
    CURRENT_TEMP = 0
    CURRENT_HUMIDITY = 0
    UPDATE_LOOP = 100
    def __init__(self):
        self.CURRENT_TEMP = 0
        self.CURRENT_HUMIDITY = 0

    def update(self):
        try:
            while True :
                result = instance.read()
                if(result.is_valid()) :
                    print("Last valid input: " + str(datetime.datetime.now()))
                    print("Temperature: %d C" % result.temperature)
                    print("Humidity: %d %%" % result.humidity)
                self.CURRENT_TEMP = result.temperature
                self.CURRENT_HUMIDITY = result.humidity
                time.sleep(UPDATE_LOOP)
        except KeyboardInterrupt:
            print("Cleanup GPIO")
            GPIO.cleanup()
    def getTemp(self) :
        return self.CURRENT_TEMP
    def getHumidity(self) :
        return self.CURRENT_HUMIDITY
    def setUpdateLoop(self, loop) :
        self.UPDATE_LOOP = loop


