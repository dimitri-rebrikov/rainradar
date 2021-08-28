import network
import time
from exception import RainradarException

def connect(ssid, password):
    sta_if = network.WLAN(network.STA_IF)
    print('connecting to network...')
    sta_if.active(True)
    sta_if.connect(ssid, password)
    tries = 0
    while not sta_if.isconnected():
        tries = tries + 1
        if tries > 10:
            print("no wifi connection after 10 sec")
            raise RainradarException("WFER")
        time.sleep(1)       

    print('network config:', sta_if.ifconfig())
