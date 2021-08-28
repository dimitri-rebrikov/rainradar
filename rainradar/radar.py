import urequests as requests
from exception import RainradarException

url='https://morgenwirdes.de/api/v2/rjson.php?plz='

class Radar:
    def __init__(self, plz):
        self.url = url + str(plz)

    def getData(self):
        try:
            r = requests.get(self.url)
            try:
                records = r.json()
            except:
                raise RainradarException("RDJS")
            r.close()
        except:
            raise RainradarException("RDGT")
        dbzList = []
        for record in records:
            dbzList.append(int(float(record['dbz'])))
        return dbzList
