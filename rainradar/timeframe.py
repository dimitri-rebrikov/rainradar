class TimeFrame:

    def __init__(self, timeFrame):
        hourMinuteBegin, hourMinuteEnd = timeFrame.split('-')
        self.timeBegin = TimeFrame.__convert_to_decimal(hourMinuteBegin.strip())
        self.timeEnd = TimeFrame.__convert_to_decimal(hourMinuteEnd.strip())


    @staticmethod
    def __convert_to_decimal(timeStr):
        hour, min = tuple(timeStr.split(':'))
        converted = float(hour) + (float(min)/60)
        #print(timeStr + "->" + str(converted))
        return converted


    def isInFrame(self, hourMinute):
        time = TimeFrame.__convert_to_decimal(hourMinute)
        if self.timeBegin < self.timeEnd:
            return time >= self.timeBegin and time <= self.timeEnd
        elif self.timeBegin > self.timeEnd:
            return ( time >= self.timeBegin and time <= 24 )\
                or ( time <= self.timeEnd )
        else:
            return time == self.timeBegin


if __name__ == "__main__":
    print("6:08 - 15:30")
    timeFrame = TimeFrame("6:08 - 15:30")
    print("5:35", timeFrame.isInFrame("5:35"))
    print("10:15", timeFrame.isInFrame("10:15"))
    print("18:05 - 04:20")
    timeFrame = TimeFrame("18:05 - 04:20")
    print("3:35", timeFrame.isInFrame("3:35"))
    print("10:15", timeFrame.isInFrame("10:15"))
    print("16:15", timeFrame.isInFrame("16:15"))
    print("19:10", timeFrame.isInFrame("19:10"))