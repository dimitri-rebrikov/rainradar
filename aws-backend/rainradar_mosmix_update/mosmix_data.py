import csv
import io
from dwd_utils import mosmix
from dwd_utils.poi2MosmixMap import poi2MosmixMap
from datetime import datetime

def mosmixDataTimeStamp():
    return datetime.strptime(mosmix.MosmixData().getMosmixDataTimestamp(), 
        #Fri, 27 Mar 2015 08:05:42 GMT
        '%a, %d %b %Y %X %Z')

def mosmixDataStream():
    mosmixData = mosmix.MosmixData().getStationsDataByIds(set(poi2MosmixMap.values()), {'ww'}, range(3,9))
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
                    map(lambda ww: wwToLevel(int(float(ww))) + 1,
                        map(lambda forecast: forecast['values']['ww'],
                            mosmixData[latLon]['forecasts'],
                            ))))

# see https://www.dwd.de/DE/leistungen/opendata/help/schluessel_datenformate/kml/mosmix_element_weather_xls.xlsx
wwToLevelMap = {
    95:3,
    57:5,
    56:2,
    67:5,
    66:2,
    86:5,
    85:2,
    84:5,
    83:2,
    82:6,
    81:5,
    80:2,
    75:6,
    73:4,
    71:2,
    69:5,
    68:2,
    55:6,
    53:4,
    51:2,
    65:6,
    63:4,
    61:2,
    49:0,
    45:0,
    3:0,
    2:0,
    1:0,
    0:0
}

def wwToLevel(ww):
    if ww in wwToLevelMap:
        return wwToLevelMap[ww]
    else:
        return 0


def levelToMatrix(level):
    if level > 8:
        level = 8
    matrix = ['1' for i in range(level)]
    matrix.extend(['0' for i in range(8 - level)])
    return ''.join(matrix)


if __name__ == "__main__":
    print(mosmixDataTimeStamp())
    with mosmixDataStream() as file:
       for row in csv.reader(file):
           if row[0] == '70599':
               print(row)

