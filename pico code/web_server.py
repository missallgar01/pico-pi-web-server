import network
import socket
from time import sleep
from picozero import pico_temp_sensor, pico_led
import machine
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
        sleep(1)
    
    ip = wlan.ifconfig()[0]
    print(f'Connected on {ip}')
    return f'Connected on {ip}'

def open_socket(ip):
    # Open a socket
    address = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
    connection = socket.socket()
    connection.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    connection.bind(address)
    connection.listen(1)
    print('listening on', address)
    return connection

def serve(connection):
    #Start a web server
    state = 'OFF'
    pico_led.off()
    temperature = 0
    while True:
        client = connection.accept()[0]
        request = client.recv(1024)
        request = str(request)
        try:
            request = request.split()[1]
        except IndexError:
            pass
        
        temperature = pico_temp_sensor.temp
        
        #requests from client via url
        
        if request =='/dashboard':
            html = dashboard(temperature, state)
        else:
            html = homepage()
            
        if request == '/dashboard/lighton?':
            pico_led.on()
            state = 'ON'
            html = dashboard(temperature, state)
        elif request =='/dashboard/lightoff?':
            pico_led.off()
            state = 'OFF'
            html = dashboard(temperature, state)
        
        client.send(html)
        client.close()

def homepage():
    #Template HTML
    html = """<!DOCTYPE html>
            <html>
            <head>
            <style>body {background-color: lightblue;}
            </style>
            </head>
            <body>
            <h1>Homepage</h1>
            <p>
            <a href="./dashboard">Link to dashboard </a>
            </p>
            </body>
            </html>
            """
    return str(html)

def dashboard(temperature, state):
    #Template HTML
    html = """<!DOCTYPE html>
            <html>
            <head>
            <style>body {background-color: lightblue;}
            </style>
            </head>
            <body>
            <h1>Dashboard</h1>
            <hr>
            
            <p><a href="./homepage">Link homepage </a></p>
            
            <form action="./dashboard/lighton">
            <input type="submit" value="Light on" />
            </form>
            <form action="./dashboard/lightoff">
            <input type="submit" value="Light off" />
            </form>
            <p>LED is """ + str(state) + """</p>
            <p>Temperature is """ + str(temperature) + """</p>
            </body>
            </html>
            """
    return str(html)

try:
    ip = connect()
    connection = open_socket(ip)
    serve(connection)
    
except KeyboardInterrupt:
    machine.reset()
    
