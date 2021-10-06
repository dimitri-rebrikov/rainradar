try:
  import ujson as json
except:
  import json

from exception import RainradarException

filePath="config.json"

class Config:
    def __init__(self):
        self.config = {
            'ssid':'change_me',
            'password':'change_me',
            'plz':'change_me'
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
        return self.config['ssid']
    
    def setSsid(self, ssid):
        self.config['ssid'] = ssid
    
    def getPassword(self):
        return self.config['password']
    
    def setPassword(self, password):
        self.config['password'] = password
    
    def getPlz(self):
        return self.config['plz']
    
    def setPlz(self, plz):
        self.config['plz'] = plz
