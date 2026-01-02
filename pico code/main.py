import network
import time
from machine import Pin
import requests, json
from secrets import secrets
#import uasyncio as asyncio #test if not needed

ssid = secrets['ssid']
password = secrets['pw']


def connect():
    #Connect to WLAN
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    while wlan.isconnected() == False:
        print('Waiting for connection...')
        time.sleep(1)
    
    ip = wlan.ifconfig()[0]
    print(f'Connected on {ip}')
    return f'Connected on {ip}'


connect()

data_from_pi = {'temp_1': 105, 'temp_2': 150}
response = requests.post('http://192.168.1.177:5000/pi', json=data_from_pi)
