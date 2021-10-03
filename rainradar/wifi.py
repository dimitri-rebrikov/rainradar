import network
import time
from exception import RainradarException

sta_if = network.WLAN(network.STA_IF)
ap_if = network.WLAN(network.AP_IF)

def connect(ssid, password, wait=True):
    print('connecting to network...')
    sta_if.active(True)
    sta_if.disconnect()
    sta_if.connect(ssid, password)
    tries = 0
    if wait:
        while not sta_if.isconnected():
            tries = tries + 1
            if tries > 10:
                print("no wifi connection after 10 sec")
                raise RainradarException("ERR WIFI")
            time.sleep(1)       
    else:
        print("connected: " + str(sta_if.isconnected()))
    print('network config:', sta_if.ifconfig())
    
def disconnect():
    sta_if.disconnect()
    
def isConnected():
    return sta_if.isconnected()

def listNetworks():
    sta_if.active(True)
    networks = sorted(sta_if.scan(), key=lambda entry: entry[3], reverse=True) # pos 3 is the signal strength
    nameList = []
    for network in networks:
        name = network[0].decode('utf-8')
        if len(name) != 0 and not name in nameList :
            nameList.append(name)
    return nameList
    
def startAccessPoint():
    print('start access point')
    ap_if.active(True)
    ap_if.config(essid="rainradar", password="rainradar2021", authmode=3)
    while not ap_if.active():
        pass
    
def stopAccessPoint():
    print('stop access point')
    ap_if.active(False)