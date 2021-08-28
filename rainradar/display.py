import max7219
from machine import Pin, SPI

radar_start_x = 0
radar_max_x = 29

time_x = 31

max_y = 8

class WeatherDisplay:
    def __init__(self):
        spi = SPI(1, baudrate=10000000, polarity=0, phase=0)
        self.disp = max7219.Matrix8x8(spi, Pin(15), 4)
        self.disp.brightness(0)
        self.clean()

    def showRainLevels(self, levelList):
        print("showRainLevels: " + repr(levelList))
        if self.needClean:
            self.clean()
        else:
            # clean the radar area only
            self.disp.fill_rect(radar_start_x, 0, radar_max_x - radar_start_x + 1, max_y, 0)
        # iterate over dbZ values and show them as bars
        for i in range(min(len(levelList), radar_max_x - radar_start_x)):
            level = levelList[i] + 1 # display no rain a bar with one element
            self.disp.vline(radar_start_x + i, max(max_y - level, 0), level, 1)
        self.disp.show()
        
    def showWaitTime(self, toWait):
        if self.needClean:
            self.clean()
        else:
            # clean the time bar
            self.disp.vline(time_x, 0, 8, 0)
        # show the time bar
        self.disp.vline(time_x, max(8 - toWait, 0), toWait, 1)
        self.disp.show()

    def showText(self, text):
        print("showText: " + text)
        self.disp.fill(0)
        self.disp.text(text, 0, 0)
        self.disp.show()
        self.needClean = True;
        
    def clean(self):
        self.disp.fill(0)
        self.disp.show()
        self.needClean = False