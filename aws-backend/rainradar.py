from dwd_utils import mosmix, plz, radolan


def rainradarForPlz(plzStr):
    plzInt = int(plzStr)
    assert plzInt in plz.plzMap, 'unknown PLZ "' + str(plzStr) + '"'
    plzInfo = plz.plzMap[plzInt]
    # print(plzInfo)
    return rainradarForCoord(lat=plzInfo['lat'], lon=plzInfo['lon'])


def rainradarForCoord(lat, lon):
    radolanData = radolan.RadolanProducts.getLatestRvData(lat=float(lat), lon=float(lon))
    # print(radolanData)
    return list(map(lambda lev: levelToMatrix(lev),\
        map(lambda mm: mmToLevel(mm),\
            map(lambda el: el['value'],\
                radolanData['forecasts']))))


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
    matrix = [1 for i in range(level)]
    matrix.extend([0 for i in range(8 - level)])
    return matrix


if __name__ == "__main__":
    # for level in range(9):
    #     print(str(level) + '->' + str(levelToMatrix(level)))
    #
    print(rainradarForPlz(30159))
    #
    # print(rainradarForCoord(52.390248580034914, 9.769367872749202))
    #
    # print(rainradarForCoord(43.89942403733628, 21.309042123149187))
    #
    # print(rainradarForCoord(46.6195770132862, -0.5553209134086552))

    

