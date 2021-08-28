import ujson
from exception import RainradarException

filePath="config.json"

class Config:
    def __init__(self):
        try:
            fp = open(filePath, 'r')
        except:
            raise RainradarException("CFRD")
        else:
            with fp:
                try:
                    self.config=ujson.load(fp)
                except:
                    raise RainradarException("CFJS")
    
    def writeConfig(self):
        with open(filePath, 'w') as fp:
            return ujson.dump(self.config, fp)
        
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
    