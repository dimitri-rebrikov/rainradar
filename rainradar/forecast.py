import urequests as requests
from exception import RainradarException
import gc
from ucollections import OrderedDict

url='https://morgenwirdes.de/api/v2/mosjson.php?plz='

typesToLevels = {
    "R101": 1,
    "R110": 2,
    "R130": 3,
    "R150": 4,
    "RR1o1": 5,
    "RR1w1": 6,
    "RR1u1": 7
}

class Forecast:
    
    def __init__(self, plz):
        self.url = url + str(plz)

    def getRainForecastForType(self, type):
        try:
            r = requests.get(self.url + '&type='  + type)
            try:
                records = r.json()['data']
            except Exception as e:
                print(repr(e))
                raise RainradarException("WRONG JSON FORECAST")
            r.close()
        except Exception as e:
            print(repr(e))
            raise RainradarException("WEB CANNOT GET FORECAST")
        forecastList = []
        max = 24
        cnt = 0
        for record in records:
            #print("type: " + type + ", record: " + repr(record))
            gc.collect()
            forecastList.append({ 'timestamp' : int(record['time']), 'probability' : int(float(record['data'])) })
            cnt += 1
            if cnt > max:
                break;
        return forecastList

    def getRainForecast(self):
        forecast = OrderedDict()
        for type in typesToLevels.keys():
            fct = self.getRainForecastForType(type)
            for fctRec in fct:
                if not fctRec['timestamp'] in forecast or forecast[fctRec['timestamp']]['probability'] <= fctRec['probability']:
                    forecast[fctRec['timestamp'] ] =  { 'probability':fctRec['probability'], 'level':typesToLevels[type] }
        print("forecast: " + repr(forecast));
        return forecast
    
    def getRainLevels(self):
        levels = []
        forecast = self.getRainForecast()
        for timestamp, elem in forecast.items():
                levels.append({
                    'timestamp':timestamp,
                    'level': elem['level'] if elem['probability'] >= 50 else 0
                })
        print("forecast levels: " + repr(levels))
        return levels
            
            

