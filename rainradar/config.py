import ujson

filePath="config.json"

class Config:
    def __init__(self):
        with open(filePath, 'r') as fp:
            self.config=ujson.load(fp)
    
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
    
