import urequests as requests

url='https://morgenwirdes.de/api/v2/rjson.php?plz='

class Radar:
    def __init__(self, plz):
        self.url = url + str(plz)

    def getData(self):
        r = requests.get(self.url)
        records = r.json()
        r.close()
        dbzList = []
        for record in records:
            dbzList.append(int(float(record['dbz'])))
        return dbzList
