import sys
import os

import RPi.GPIO as GPIO
import dht11
import time
import datetime

tempsensor_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "lib", "tempsensor"))
sys.path.append(tempsensor_path)
#Why path not working?
import tempsensor_setup
import tempsensor

GPIO.setwarnings(True)
GPIO.setmode(GPIO.BCM)
PIN = 4 #Placeholder
instance = dht11.DHT11(PIN)

class TEMP_STAT : 
    def __init__(self):
        self.CURRENT_TEMP = 0
        self.CURRENT_HUMIDITY = 0
        self.UPDATE_LOOP = 100
        self.NEW_TEMP = False
        self.NEW_HUMIDITY = False
        self.update()
    
    def __del__(self) : 
        GPIO.cleanup()

    def update(self):
        try:
            while True :
                result = instance.read()
                if result.is_valid() :
                    print("Last valid input: " + str(datetime.datetime.now()))
                    print("Temperature: %d C" % result.temperature)
                    print("Humidity: %d %%" % result.humidity)
                if self.CURRENT_TEMP == result.temperature and self.CURRENT_HUMIDITY == result.humidity :
                    continue
                elif self.CURRENT_TEMP != result.temperature :
                    self.CURRENT_TEMP = result.temperature
                    self.NEW_TEMP = True
                    print("Temp: %d", self.CURRENT_TEMP)
                elif self.CURRENT_HUMIDITY != result.humidity :
                    self.CURRENT_HUMIDITY = result.humidity
                    self.NEW_HUMIDITY = True
                    print("Humidity: %d %%", self.CURRENT_HUMIDITY)
                time.sleep(self.UPDATE_LOOP)
        except KeyboardInterrupt:
            print("Cleanup GPIO")
            GPIO.cleanup()
    def getTemp(self) :
        if(self.NEW_TEMP) : 
            self.NEW_TEMP = False
            return self.CURRENT_TEMP
        else : 
            return self.CURRENT_TEMP
    def getHumidity(self) :
        if(self.NEW_HUMIDITY) :
            self.NEW_HUMIDITY = False  
            return self.CURRENT_HUMIDITY
    def setUpdateLoop(self, loop) :
        self.UPDATE_LOOP = loop


