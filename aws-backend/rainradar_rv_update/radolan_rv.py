import csv
import io
from dwd_utils import radolan_hdf5
from dwd_utils.poi2RadolanHdf5RvMap import poi2RadolanHdf5RvMap
from datetime import datetime

def radolanRvTimeStamp():
    return datetime.strptime(radolan_hdf5.RadolanHdf5Products.getLatestRvDataTimestamp(), 
        #Fri, 27 Mar 2015 08:05:42 GMT
        '%a, %d %b %Y %X %Z')

def radolanRvDataStream():
    radolanData = radolan_hdf5.RadolanHdf5Products.getLatestRvData(set(convertXyToXyXy(poi2RadolanHdf5RvMap.values())))
    f = io.StringIO()
    csv_writer = csv.writer(f)
    for k in poi2RadolanHdf5RvMap:
        a = []
        a.append(k)
        a.extend(extractForecastsForCoord(poi2RadolanHdf5RvMap[k], radolanData))
        csv_writer.writerow(a)
    f.seek(0)
    return f

def convertXyToXyXy(xyList):
    xyxyList = []
    for xy in xyList:
        xyxyList.append((xy[0], xy[1], xy[0], xy[1]))
    return xyxyList


def extractForecastsForCoord(coord, radolanData):
    return list(map(lambda lev: levelToMatrix(lev),\
        map(lambda mm: mmToLevel(mm) + 1,\
            map(lambda el: el['values'][coord],\
                radolanData['forecasts'][:24]))))


def mmToLevel(mm):
    if(mm < 0):
        return -1 # no value
    elif(mm < 0.1):
        return 0 # no rain
    elif(mm < 1.2):
        return 1 # very light rain
    elif(mm < 2.5):
        return 2 # light rain
    elif(mm < 5.5):
        return 3 # light to moderate rain
    elif(mm < 10):
        return 4 # moderate rain
    elif(mm < 25):
        return 5 # moderate to heavy rain
    elif(mm < 50):
        return 6 # heavy rain
    else:
        return 7 # very heavy rain


def levelToMatrix(level):
    if level > 8:
        level = 8
    matrix = ['1' for i in range(level)]
    matrix.extend(['0' for i in range(8 - level)])
    return ''.join(matrix)


if __name__ == "__main__":
    print(radolanRvTimeStamp().isoformat())
    with radolanRvDataStream() as file:
       for row in csv.reader(file):
           if row[0] == '24944':
               print(row)


    

