import max7219
from machine import Pin, SPI
import framebuf
import time

radar_start_x = 0
radar_max_x = 29

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
