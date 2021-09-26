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

syncTimePeriod = 60*60 # 1 hour
embUnixTimeDiff = 946684800 # embedded systems use 01-01-2000 as start of the time in compare to the unix' 01-01-1970

def syncTime():
    global syncTimePeriod, lastSyncTime
    if lastSyncTime == 0 or lastSyncTime < time.time() - syncTimePeriod:
        ntptime.settime()
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
        print("minutes to wait: " + str(minutesToWait))
        for i in range(0, minutesToWait):
            disp.infoLed(0)
            time.sleep(0.5)
            disp.infoLed(1)
            time.sleep(0.5)
        time.sleep(minutesToWait/2 + 1)
    
# main loop
while True:
    disp = Display()
    lastSyncTime = 0
    nextRadarSyncTime = 0
    nextForecastSyncTime = 0
    try:
        cfg = Config()
        plz = cfg.getPlz()
        disp.showText(plz, 2)
        wifi.connect(cfg.getSsid(), cfg.getPassword())
        radar = Radar(plz)
        weather = Weather(plz)
        while True:
            syncTime()
            updateRainRadarLevels()
            print("nextForecastSyncTime:"+str(emb2UnixTime(nextForecastSyncTime))+", time:"+str(emb2UnixTime(time.time())))
            if nextForecastSyncTime <= time.time():
                updateRainForecastLevels()
            showPause()

    except RainradarException as exp:
        disp.showText(str(exp), 3)
