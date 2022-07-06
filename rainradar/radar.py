import urequests as requests
from exception import RainradarException

url='https://yjatpjzqik.execute-api.eu-west-1.amazonaws.com/rainradar_get?plz='

class Radar:
    def __init__(self, plz):
        self.url = url + str(plz)

    def getLevelList(self):
        try:
            r = requests.get(self.url)
            try:
                records = r.json()
            except Exception as e:
                print(repr(e))
                raise RainradarException("ERR JSON RADAR")
            r.close()
        except Exception as e:
            print(repr(e))
            raise RainradarException("ERR GET RADAR")
        recordList = []
        for record in records:
            recordList.append(record)
        return recordList
