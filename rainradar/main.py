import time
from display import Display
from radar import Radar
import wifi
from config import Config
from exception import RainradarException
import ntptime
import math
import rain
from weather import Weather
from config_changer import ConfigChanger
import machine
import urandom
import gc
import sys

syncTimePeriod = 60*60 # 1 hour
embUnixTimeDiff = 946684800 # embedded systems use 01-01-2000 as start of the time in compare to the unix' 01-01-1970

configMode = 0

def bootButtonCallback(pin):
  global configMode
  print("boot button pressed")
  configMode = 1
  
bootButton = machine.Pin(0, machine.Pin.IN, machine.Pin.PULL_UP)
bootButton.irq(trigger=machine.Pin.IRQ_FALLING, handler=bootButtonCallback)

def syncTime():
    global syncTimePeriod, lastSyncTime
    logCurrentTime()
    if lastSyncTime == 0 or lastSyncTime < time.time() - syncTimePeriod:
        try:
            ntptime.settime()
        except Exception as e:
            print(repr(e))
            raise RainradarException("ERR NTP")
        print("Synced time with NTP server")
        logCurrentTime()
        lastSyncTime = time.time()
        
def emb2UnixTime(embTime):
    return embTime + embUnixTimeDiff

def unix2EmbTime(unixTime):
    return unixTime - embUnixTimeDiff

def logCurrentTime():
    print("Current time: UTC:" + formatTimeArr(time.gmtime()) + ", local:" + formatTimeArr(time.localtime()) + ", unix:" + str(emb2UnixTime(time.time())) + ", embedded:" + str(time.time()))
    
def formatTimeArr(arr):
    return str(arr[0]) + "-" + str(arr[1]) + "-" + str(arr[2]) + " " + str(arr[3]) + ":" + str(arr[4]) + ":" + str(arr[5])
        
def updateRainRadarLevels():
    mmRecordList = removePastRecords(radar.getMmRecordList(), 0)
    print("rain radar records: " + repr(mmRecordList))
    levelList = rain.mmRecordListToLevelList(mmRecordList)
    disp.showRainLevels(levelList)
    setNextRadarSyncTime(mmRecordList)
    
def updateRainForecastLevels():
    forecastList = removePastRecords(weather.getRainHourlyForecast(), 60 * 60 * 2)
    print("rain forecast records: " + repr(forecastList))
    levelList = rain.mmRecordListToLevelList(forecastList)
    disp.showForecastLevels(levelList)
    setNextForecastSyncTime(forecastList)
    
def removePastRecords(timestampRecordList, addFutureSeconds):
     #print("unixTime:" + str(unixTime(time.time())))
     #print("beforFilter: " + repr(timestampRecordList))
     return list(filter(lambda rec: rec['timestamp'] >= emb2UnixTime(time.time()+ addFutureSeconds), timestampRecordList))
    
def getRandomInt(base):
    return int(urandom.random() * base)
    
def setNextRadarSyncTime(mmRecordList):
    global nextRadarSyncTime
    if len(mmRecordList) < 1:
        nextRadarSyncTime = time.time() + ( 5 * 60 ) + getRandomInt(10)
    else:
        nextRadarSyncTime = unix2EmbTime(mmRecordList[0]['timestamp']) + 15 + getRandomInt(10)
        
def setNextForecastSyncTime(forecastList):
    global nextForecastSyncTime
    if len(forecastList) < 1:
        nextForecastSyncTime = time.time() + ( 60 * 60 )
    else:
        nextForecastSyncTime = unix2EmbTime(forecastList[0]['timestamp']) - (60 * 60 * 3) + getRandomInt(20)
   
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
    lastSyncTime = 0
    nextRadarSyncTime = 0
    nextForecastSyncTime = 0
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
        weather = Weather(plz)
        while True:
            syncTime()
            checkConfigMode()
            updateRainRadarLevels()
            print("nextForecastSyncTime:"+str(emb2UnixTime(nextForecastSyncTime))+", time:"+str(emb2UnixTime(time.time())))
            checkConfigMode()
            if nextForecastSyncTime <= time.time():
                updateRainForecastLevels()
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
