import urequests as requests
from exception import RainradarException

url='https://morgenwirdes.de/api/v2/rjson.php?plz='

class Radar:
    def __init__(self, plz):
        self.url = url + str(plz)

    def getMmRecordList(self):
        try:
            r = requests.get(self.url)
            try:
                records = r.json()
            except Exception as e:
                print(repr(e))
                raise RainradarException("WRONG JSON RADAR")
            r.close()
        except Exception as e:
            print(repr(e))
            raise RainradarException("WEB CANNOT RADAR")
        mmRecordList = []
        for record in records:
            mmRecordList.append({'mm':float(record['mm']), 'timestamp':int(record['timestamp'])})
        return mmRecordList
