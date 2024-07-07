import tm1637
import urequests
from machine import Pin
from utime import sleep
import network

mydisplay = tm1637.TM1637(clk=Pin(0), dio=Pin(1))
mydisplay.brightness(2)

api_url = 'http://api.cskartikey.hackclub.app/data'

ssid = 'ssid'
password = 'password'

def connect(ssid, password, timeout=20):
    """
    Connect to WLAN within a timeout period.
    """
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    mydisplay.number(3)

    elapsed_time = 0
    while not wlan.isconnected():
        if elapsed_time > timeout:
            print('Connection timeout.')
            mydisplay.number(9)
            return False
        print('Connecting...')
        sleep(1)
        elapsed_time += 1

    print('Connected:', wlan.ifconfig())
    mydisplay.show("Connected")
    return True

def get_data(url):
    try:
        mydisplay.scroll("requesting")
        response = urequests.get(url)
        if response.status_code == 200:
            print('Data retrieved:', response.json())
            res_json = response.json()
            mydisplay.number(res_json['total_users'])
        else:
            print('Failed with status', response.status_code)
            mydisplay.number(8)
    except Exception as e:
        print('Request failed:', e)
        mydisplay.number(7)

def main():
    if connect(ssid, password):
        get_data(api_url)

main()
