import time
from display import Display
from radar import Radar
import wifi
from config import Config
from exception import RainradarException
import ntptime
import math
from config_changer import ConfigChanger
import machine
import urandom
import gc
import sys
import timeframe

syncTimePeriod = 60*60 # 1 hour

configMode = 0

def log(text):
    print(getCurrentTime() + ": " + text)

def bootButtonCallback(pin):
  global configMode
  log("boot button pressed")
  configMode = 1
  
bootButton = machine.Pin(0, machine.Pin.IN, machine.Pin.PULL_UP)
bootButton.irq(trigger=machine.Pin.IRQ_FALLING, handler=bootButtonCallback)

def syncTime():
    global syncTimePeriod, lastSyncTime
    if lastSyncTime == 0 or lastSyncTime < time.time() - syncTimePeriod:
        log("Syncing time...")
        try:
            ntptime.settime()
        except Exception as e:
            log(repr(e))
            raise RainradarException("ERR NTP")
        log("Synced time with NTP server")
        lastSyncTime = time.time()

def getCurrentTime():
    return formatEmbTime(time.time()) + " UTC"

def formatEmbTime(embTime):
    return '{:04d}-{:02d}-{:02d} {:02d}:{:02d}:{:02d}'.format(*time.gmtime(embTime))

def setBrightness(disp, brightness, brightnessNight, timeNight):
    try:
        if brightnessNight != None and timeNight != None:
            curTime = str(time.gmtime()[3]) + ':' + str(time.gmtime()[4])
            if timeframe.TimeFrame(timeNight).isInFrame(curTime):
                log("set night time brightness: " + str(brightnessNight))
                disp.setBrightness(brightnessNight)
                return
        if brightness == None:
            brightness = 10
        log("set daytime brightness: " + brightness)
        disp.setBrightness(brightness)
    except Exception as exp:
        log("setBrightness Exception: " + str(exp))
        sys.print_exception(exp)
    
def updateRainRadarLevels():
    levelList = radar.getLevelList()
    log("rain radar records:")
    logLevels(levelList)
    disp.showRainLevels(levelList)
    setNextRadarSyncTime()
    
def logLevels(levelList):
    log(",".join(levelList))

def getRandomInt(base):
    return int(urandom.random() * base)
    
def setNextRadarSyncTime():
    global nextRadarSyncTime
    nextRadarSyncTime = time.time() + ( 5 * 60 ) + getRandomInt(10)
 
def showPause():
    log("Pause for " + str(nextRadarSyncTime - time.time()) + " seconds.")
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
    #log("Config mode: " + str(configMode))
    if configMode != 0:
        log("Starting config changer...")
        configChanger.startServer()
        log("Config changer finished.")
        configMode = 0
        raise RainradarException("CONF EXIT")
    
def garbageCollector():
    gc.collect()
    log("Free memory: " + str(gc.mem_free()))
    
# main loop
while True:
    disp = Display()
    lastSyncTime = 0
    nextRadarSyncTime = 0
    try:
        cfg = Config()
        configChanger = ConfigChanger(cfg, disp)
        try:
            cfg.readConfig()
        except RainradarException as exp:
            log("Exception in readConfig: " + str(exp))
            configMode = 1
        checkConfigMode()
        plz = cfg.getPlz()
        disp.showText(plz, 2)
        checkConfigMode()
        wifi.connect(cfg.getSsid(), cfg.getPassword())
        radar = Radar(plz)
        while True:
            syncTime()
            setBrightness(disp, cfg.getBrightness(), cfg.getBrightnessNight(), cfg.getTimeNight())
            checkConfigMode()
            updateRainRadarLevels()
            checkConfigMode()
            showPause()
            garbageCollector()

    except RainradarException as rexp:
        strExp = str(rexp)
        log("RainradarException: " + strExp)
        disp.showText(strExp, 3)
        garbageCollector()
    except Exception as exp:
        strExp = str(exp)
        log("Unknown Exception: " + strExp)
        sys.print_exception(exp)
        while True: # stick on showing unknown exception
            disp.showText(strExp, 3)
            garbageCollector()
