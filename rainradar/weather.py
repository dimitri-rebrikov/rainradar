import urequests as requests
from exception import RainradarException

url='https://morgenwirdes.de/api/v2/mosjson.php?plz='

typeRainForecastHourly = "RR1c"

class Weather:
    
    def __init__(self, plz):
        self.url = url + str(plz)

    def getRainHourlyForecast(self):
        try:
            r = requests.get(self.url + '&type='  + typeRainForecastHourly)
            try:
                records = r.json()['data']
            except Exception as e:
                print(repr(e))
                raise RainradarException("ERR JSON RAIN")
            r.close()
        except Exception as e:
            print(repr(e))
            raise RainradarException("ERR GET RAIN")
        forecastList = []
        max = 24
        cnt = 0
        for record in records:
            #print("type: " + type + ", record: " + repr(record))
            forecastList.append({ 'timestamp' : int(record['time']), 'mm' : float(record['data']) })
            cnt += 1
            if cnt > max:
                break;
        return forecastList