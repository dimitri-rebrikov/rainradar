import time
from display import Display
from radar import Radar
import wifi
from config import Config
from exception import RainradarException
import ntptime
import math
import rain

syncTimePeriod = 60*60 # 1 hour
lastSyncTime = 0

embUnixTimeDiff = 946684800

nextMmSyncTime = time.time()

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
    mmRecordList = removePastRecords(radar.getMmRecordList())
    print("rain records: " + repr(mmRecordList))
    levelList = rain.mmRecordListToLevelList(mmRecordList)
    disp.showRainLevels(levelList)
    setNextMmSyncTime(mmRecordList)
    
def removePastRecords(timestampRecordList):
     #print("unixTime:" + str(unixTime(time.time())))
     #print("beforFilter: " + repr(timestampRecordList))
     return list(filter(lambda rec: rec['timestamp'] >= emb2UnixTime(time.time()), timestampRecordList))
    
def setNextMmSyncTime(mmRecordList):
    global nextMmSyncTime
    if len(mmRecordList) < 1:
        nextMmSyncTime = time.time() + ( 5 * 60 )
    else:
        nextMmSyncTime = unix2EmbTime(mmRecordList[0]['timestamp']) + 15
            
def showPause():
    while(nextMmSyncTime > time.time()):
        minutesToWait = math.ceil( (nextMmSyncTime - time.time()) / 60 )
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
        while True:
            syncTime()
            updateRainLevels()
            showPause()

    except RainradarException as exp:
        disp.showText(str(exp), 2)
