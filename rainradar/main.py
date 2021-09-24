import time
from display import Display
from radar import Radar
import wifi
from config import Config
from exception import RainradarException
import ntptime
import math
import rain
from forecast import Forecast

syncTimePeriod = 60*60 # 1 hour
lastSyncTime = 0

embUnixTimeDiff = 946684800

nextRadarSyncTime = 0

nextForecastSyncTime = 0

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
        
def updateRainLevels():
    mmRecordList = removePastRecords(radar.getMmRecordList(), 0)
    print("rain records: " + repr(mmRecordList))
    levelList = rain.mmRecordListToLevelList(mmRecordList)
    disp.showRainLevels(levelList)
    setNextRadarSyncTime(mmRecordList)
    
def updateForecastLevels():
    forecastList = removePastRecords(forecast.getRainLevels(), 60 * 60 * 3)
    print("forecast records: " + repr(forecastList))
    levelList = []
    for rec in forecastList:
        levelList.append(rec['level'])
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
        time.sleep(1)
        disp.showWaitTime(minutesToWait-1)
        time.sleep(1)
    
# main loop
while True:
    disp = Display()
    try:
        cfg = Config()
        plz = cfg.getPlz()
        disp.showText(plz, 2)
        wifi.connect(cfg.getSsid(), cfg.getPassword())
        radar = Radar(plz)
        forecast = Forecast(plz)
        while True:
            syncTime()
            updateRainLevels()
            print("nextForecastSyncTime:"+str(emb2UnixTime(nextForecastSyncTime))+", time:"+str(emb2UnixTime(time.time())))
            if nextForecastSyncTime <= time.time():
                updateForecastLevels()
            showPause()

    except RainradarException as exp:
        disp.showText(str(exp), 2)

