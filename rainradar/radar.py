import urequests as requests
from exception import RainradarException

url='https://morgenwirdes.de/api/v2/rjson.php?plz='

class Radar:
    def __init__(self, plz):
        self.url = url + str(plz)

    def getMmList(self):
        try:
            r = requests.get(self.url)
            try:
                records = r.json()
            except Exception as e:
                print(repr(e))
                raise RainradarException("WRONG JSON WEB")
            r.close()
        except Exception as e:
            print(repr(e))
            raise RainradarException("WEB CANNOT GET")
        mmList = []
        for record in records:
            mmList.append(float(record['mm']))
        return mmList
