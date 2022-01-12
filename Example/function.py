# -*- coding: utf-8 -*-
import RPi.GPIO as GPIO
import time
import adafruit_dht
import board
import json
import requests

dht = adafruit_dht.DHT22(board.D4)
def temperature():
    temperature = dht.temperature
    humidity = dht.humidity
    return temperature


def get_ngrok_url():
    url = "http://localhost:4040/api/tunnels"
    res = requests.get(url)
    res_unicode = res.content.decode("utf-8")
    res_json = json.loads(res_unicode)
    return res_json["tunnels"][0]["public_url"]
