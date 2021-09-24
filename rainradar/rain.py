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
    
def mmRecordListToLevelList(mmRecordList):
    levelList = []
    for mmRecord in mmRecordList:
        levelList.append(mmToLevel(mmRecord['mm']))
    return levelList
