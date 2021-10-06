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
    if lastSyncTime == 0 or lastSyncTime < time.time() - syncTimePeriod:
        try:
            ntptime.settime()
        except Exception as e:
            print(repr(e))
            raise RainradarException("ERR NTP")
        print("Synced time to: " + str(time.time()) + ", unix:" + str(emb2UnixTime(time.time())) + ", " + str(time.gmtime()))
        lastSyncTime = time.time()
        
def emb2UnixTime(embTime):
    return embTime + embUnixTimeDiff

def unix2EmbTime(unixTime):
    return unixTime - embUnixTimeDiff
        
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
    
def setNextRadarSyncTime(mmRecordList):
    global nextRadarSyncTime
    if len(mmRecordList) < 1:
        nextRadarSyncTime = time.time() + ( 5 * 60 )
    else:
        nextRadarSyncTime = unix2EmbTime(mmRecordList[0]['timestamp']) + 15
        
def setNextForecastSyncTime(forecastList):
    global nextForecastSyncTime
    if len(forecastList) < 1:
        nextForecastSyncTime = time.time() + ( 60 * 60 )
    else:
        nextForecastSyncTime = unix2EmbTime(forecastList[0]['timestamp']) - (60 * 60 * 3) + 20     
   
def showPause():
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
    
# main loop
while True:
    disp = Display()
    lastSyncTime = 0
    nextRadarSyncTime = 0
    nextForecastSyncTime = 0
    try:
        cfg = Config()
        configChanger = ConfigChanger(cfg, disp)
        checkConfigMode()
        cfg.readConfig()
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

    except RainradarException as exp:
        strExp = str(exp)
        print("RainradarException: " + strExp)
        if 'ERR CONF' in strExp:
            configMode = 1
        else:
            disp.showText(str(exp), 3)
