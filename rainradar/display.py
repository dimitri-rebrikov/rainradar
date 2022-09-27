import max7219
from machine import Pin, SPI
import framebuf
import time

start_x = 0
max_x = 30

time_x = 31

max_y = 8

class Display:
    def __init__(self):
        spi = SPI(1, baudrate=10000000, polarity=0, phase=0, sck=Pin(4), mosi=Pin(2))
        ss = Pin(5, Pin.OUT) 
        self.disp = max7219.Matrix8x8(spi, ss, 4)
        self.clean()
        self.setBrightness(0)

    def setBrightness(self, brightness):
        self.disp.brightness(int(brightness))

    def showRainLevels(self, levelList):
        print("showLevels: start: " + str(start_x) + ", max: " + str(max_x) + ", levels: "+ repr(levelList))
        if self.needClean:
            self.clean()
        else:
            # clean the required area only
            self.disp.fill_rect(start_x, 0, max_x - start_x + 1, max_y, 0)
        # iterate over values and show them as bars
        for i in range(min(len(levelList), max_x - start_x + 1)):
            level = levelList[i]
            for j in range(min(len(level), max_y)):
                try:
                    self.disp.pixel(i, max_y - 1 - j, int(level[j:j+1]))
                except Exception as exp:
                    with open("level.log", "w") as levellog:
                        print("showLevels: i: " + str(i) + ", j: " + str(j) + ", levels: ["+ repr(levelList) +"]", file=levellog)
                    raise

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

    def showText(self, text, duration=0):
        print("showText: " + text)
        if(len(text) > 4):
            self._showLongText(text, 1 if duration == 0 else duration)
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
        rainLevels=['00000000',
                    '10000000',
                    '11000000',
                    '11100000',
                    '11110000',
                    '11111000',
                    '11111100',
                    '11111110',
                    '11111111',
                    '11111110',
                    '11111100',
                    '11111000',
                    '11110000',
                    '11100000',
                    '11000000',
                    '10000000',
                    '00000000',
                    '11000000',
                    '11110000',
                    '11111100',
                    '11110000',
                    '11000000',
                    '00000000',
                    '10000000',
                    '11100000',
                    '11111110',
                    '11110000',
                    '11000000',
                    '10000000']
        for i in range(len(rainLevels)):
            self.showRainLevels(rainLevels)
            time.sleep(1)
            rainLevels.append(rainLevels.pop(0))
        for i in range(9):
            self.showWaitTime(i)
            time.sleep(1)
