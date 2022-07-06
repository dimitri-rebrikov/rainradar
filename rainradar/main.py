import time
from display import Display
from radar import Radar
import wifi
from config import Config
from exception import RainradarException
import math
from config_changer import ConfigChanger
import machine
import urandom
import gc
import sys

configMode = 0

def bootButtonCallback(pin):
  global configMode
  print("boot button pressed")
  configMode = 1
  
bootButton = machine.Pin(0, machine.Pin.IN, machine.Pin.PULL_UP)
bootButton.irq(trigger=machine.Pin.IRQ_FALLING, handler=bootButtonCallback)


def updateRainRadarLevels():
    levelList = radar.getLevelList()
    print("rain radar records:")
    logLevels(levelList)
    disp.showRainLevels(levelList)
    setNextRadarSyncTime()
    
def logLevels(levelList):
    for levelObject in levelList:
        logLevel(levelObject)

def logLevel(levelObject):
    print(levelObject)
    
def getRandomInt(base):
    return int(urandom.random() * base)
    
def setNextRadarSyncTime():
    global nextRadarSyncTime
    nextRadarSyncTime = time.time() + ( 5 * 60 ) + getRandomInt(10)
 
def showPause():
    print("Pause for " + str(nextRadarSyncTime - time.time()) + " seconds.")
    while(nextRadarSyncTime > time.time()):
        minutesToWait = math.ceil( (nextRadarSyncTime - time.time()) / 60 )
        disp.showWaitTime(minutesToWait)
        checkConfigMode()
        time.sleep(1)
        disp.showWaitTime(0)
        checkConfigMode()
        time.sleep(1)

def checkConfigMode():
    global configChanger, configMode
    #print("Config mode: " + str(configMode))
    if configMode != 0:
        print("Starting config changer...")
        configChanger.startServer()
        print("Config changer finished.")
        configMode = 0
        raise RainradarException("CONF EXIT")
    
def garbageCollector():
    gc.collect()
    print("Free memory: " + str(gc.mem_free()))
    
# main loop
while True:
    disp = Display()
    nextRadarSyncTime = 0
    try:
        cfg = Config()
        configChanger = ConfigChanger(cfg, disp)
        try:
            cfg.readConfig()
        except RainradarException as exp:
            print("Exception in readConfig: " + str(exp))
            configMode = 1
        checkConfigMode()
        plz = cfg.getPlz()
        disp.showText(plz, 2)
        checkConfigMode()
        wifi.connect(cfg.getSsid(), cfg.getPassword())
        radar = Radar(plz)
        while True:
            checkConfigMode()
            updateRainRadarLevels()
            checkConfigMode()
            showPause()
            garbageCollector()

    except RainradarException as rexp:
        strExp = str(rexp)
        print("RainradarException: " + strExp)
        disp.showText(strExp, 3)
        garbageCollector()
    except Exception as exp:
        strExp = str(exp)
        print("Unknown Exception: " + strExp)
        sys.print_exception(exp)
        while True: # stick on showing unknown exception
            disp.showText(strExp, 3)
            garbageCollector()
