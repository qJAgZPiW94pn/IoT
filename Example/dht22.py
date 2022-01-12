#!/usr/bin/python
import time
import adafruit_dht
import board
#import RPI.GPIO as GPIO
 
dht22 = adafruit_dht.DHT22(board.D4)
temperature = dht22.temperature
humidity = dht22.humidity

if humidity is not None and temperature is not None:
    print("temp:{0:0.1f}".format(temperature)) 
#    print("Humidity:{0:0.1f}".format(humidity)) 
