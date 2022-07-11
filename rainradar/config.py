try:
  import ujson as json
except:
  import json

from exception import RainradarException
from timeframe import TimeFrame
import sys

filePath="config.json"

class Config:
    def __init__(self):
        self.config = {
            'ssid':'change_me',
            'password':'change_me',
            'plz':'change_me',
            'brightness':'10',
            'brightnessNight':'1',
            'timeNight':'23:00-06:00'
            }
        
    def readConfig(self):
        try:
            fp = open(filePath, 'r')
        except Exception as e:
            print(repr(e))
            raise RainradarException("ERR CONF FILE")
        else:
            with fp:
                try:
                    self.config=json.load(fp)
                except Exception as e:
                    print(repr(e))
                    raise RainradarException("ERR CONF JSON")
    
    def writeConfig(self):
        with open(filePath, 'w') as fp:
            print("Write config: " + json.dumps(self.config))
            return json.dump(self.config, fp)
        
    def getSsid(self):
        return self.config.get('ssid')
        
    
    def setSsid(self, ssid):
        self.config['ssid'] = ssid
    
    def getPassword(self):
        return self.config.get('password')
    
    def setPassword(self, password):
        self.config['password'] = password
    
    def getPlz(self):
        return self.config.get('plz')
    
    def setPlz(self, plz):
        self.config['plz'] = plz

    def setBrightness(self, brightness):
        if Config.__brightnessOk(brightness):
            self.config['brightness'] = brightness

    def getBrightness(self):
        return self.config.get('brightness')

    def setBrightnessNight(self, brightnessNight):
        if Config.__brightnessOk(brightnessNight):
            self.config['brightnessNight'] = brightnessNight

    def getBrightnessNight(self):
        return self.config.get('brightnessNight')

    def setTimeNight(self, timeNight):
        if Config.__timeFrameOk(timeNight):
            self.config['timeNight'] = timeNight

    def getTimeNight(self):
        return self.config.get('timeNight')
    
    @staticmethod
    def __brightnessOk(brightness):
        try:
            brightness = int(brightness)
            return brightness >= 0 and brightness <=15
        except Exception as exp: 
            sys.print_exception(exp)
            return False
        
    @staticmethod
    def __timeFrameOk(timeframe):
        try:
            timeframe = TimeFrame(timeframe)
            return True
        except Exception as exp: 
            sys.print_exception(exp)
            return False
