import max7219
from machine import Pin, SPI
import framebuf
import time

radar_start_x = 0
radar_max_x = 24

forecast_start_x = 25
forecast_max_x = 30

time_x = 31

max_y = 8

class Display:
    def __init__(self):
        spi = SPI(1, baudrate=10000000, polarity=0, phase=0, sck=Pin(4), mosi=Pin(2))
        ss = Pin(5, Pin.OUT) 
        self.disp = max7219.Matrix8x8(spi, ss, 4)
        self.disp.brightness(0)
        self.clean()

    def showRainLevels(self, levelList):
        self._showLevels(levelList, radar_start_x, radar_max_x)

    def showForecastLevels(self, levelList):
        self._showLevels(levelList, forecast_start_x, forecast_max_x)
        
    def _showLevels(self, levelList, start_x, max_x):
        print("showLevels: start: " + str(start_x) + ", max: " + str(max_x) + ", levels: "+ repr(levelList))
        if self.needClean:
            self.clean()
        else:
            # clean the required area only
            self.disp.fill_rect(start_x, 0, max_x - start_x + 1, max_y, 0)
        # iterate over values and show them as bars
        for i in range(min(len(levelList), max_x - start_x + 1)):
            level = levelList[i] + 1 # display zero level as a bar with one element
            self.disp.vline(start_x + i, max(max_y - level, 0), level, 1)
        self.disp.show()
        
    def showWaitTime(self, toWait):
        if self.needClean:
            self.clean()
        else:
            # clean the time bar
            self.disp.vline(time_x, 0, 8, 0)
        if toWait != 0:
            # show the time dot
            self.disp.pixel(time_x, min(max(toWait - 1, 0), 7), 1)
        self.disp.show()

    def showText(self, text, duration):
        print("showText: " + text)
        if(len(text) > 4):
            self._showLongText(text, duration)
        else:
            self.disp.fill(0)
            self.disp.text(text, 0, 0)
            self.disp.show()
            self.needClean = True;
            time.sleep(duration)
        
    def _showLongText(self, text, duration):
        textLen = len(text)
        textFb = framebuf.FrameBuffer(bytearray(8 * textLen), 8 * textLen, 8, framebuf.MONO_HLSB)
        textFb.fill(0)
        textFb.text(text, 0, 0)
        scrollNum = (textLen - 4) * 8
        for i in range(scrollNum):
            self.disp.blit(textFb, 0, 0)
            self.disp.show()
            textFb.scroll(-1,0)
            if i == 0 or i == scrollNum - 1:
                time.sleep(duration)
            else:
                time.sleep(duration / 8)
        self.needClean = True;
        
    def clean(self):
        self.disp.fill(0)
        self.disp.show()
        self.needClean = False
        
    def test(self):
        self.showText("ABCD", 2)
        self.showText("01234567890", 2)
        rainLevels=[0, 1, 2, 3, 4, 5, 6, 7, 6, 5, 4, 3, 2, 1, 0, 2, 4, 6, 4, 2, 0, 1, 3, 7, 4, 2, 1]
        for i in range(len(rainLevels)):
            self.showRainLevels(rainLevels)
            time.sleep(1)
            rainLevels.append(rainLevels.pop(0))
        for i in range(9):
            self.showWaitTime(i)
            time.sleep(1)
