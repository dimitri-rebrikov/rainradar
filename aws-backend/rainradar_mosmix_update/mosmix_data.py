import csv
import io
from dwd_utils import mosmix
from dwd_utils.poi2MosmixMap import poi2MosmixMap


def mosmixDataStream():
    mosmixData = mosmix.MosmixData().getStationsDataByIds(set(poi2MosmixMap.values()), {'RR1c'}, range(3,9))
    f = io.StringIO()
    csv_writer = csv.writer(f)
    for k in poi2MosmixMap:
        a = []
        a.append(k)
        a.extend(extractForecastsForCoord(poi2MosmixMap[k], mosmixData))
        csv_writer.writerow(a)
    f.seek(0)
    return f


def extractForecastsForCoord(latLon, mosmixData):
    return list(map(lambda lev: levelToMatrix(lev),
                    map(lambda mm: mmToLevel(float(mm)) + 1,
                        map(lambda forecast: forecast['values']['RR1c'],
                            mosmixData[latLon]['forecasts'],
                            ))))


def mmToLevel(mm):
    if(mm < 0.1):
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
    with mosmixDataStream() as file:
       for row in csv.reader(file):
           if row[0] == '70599':
               print(row)


    

