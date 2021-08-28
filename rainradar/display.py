import max7219
from machine import Pin, SPI

radar_max_dbz = 65
radar_min_dbz = 0
radar_start_x = 0
radar_start_y = 0
radar_max_x = 29
radar_max_y = 8
radar_scale = (radar_max_dbz - radar_min_dbz) / (radar_max_y - radar_start_y - 1)

time_max = 5
time_min = 0
time_x = 31
time_start_y = 1
time_max_y = 6
time_scale = (time_max - time_min) / (time_max_y - time_start_y)

class WeatherDisplay:
    def __init__(self):
        spi = SPI(1, baudrate=10000000, polarity=0, phase=0)
        self.disp = max7219.Matrix8x8(spi, Pin(15), 4)
        self.disp.brightness(0)
        self.disp.fill(0)
        self.disp.show()

    def showRadarData(self, dbzList):
        """ The method shows the radar data

            Parameters
            ----------
            dbzList : list of int
                list of the radar dbZ's. The first is the value for now.
                The following values are forecasts.
        """
        
        # clean the radar area
        self.disp.fill_rect(radar_start_x, radar_start_y, radar_max_x - radar_start_x + 1, radar_max_y - radar_start_y + 1, 0)
        # iterate over dbZ values and show them as bars
        for i in range(min(len(dbzList), radar_max_x - radar_start_x)):
            value = max(radar_min_dbz, min(radar_max_dbz, dbzList[i]))
            scaledValue = int(value / radar_scale) + 1
            self.disp.vline(radar_start_x + i, radar_max_y - scaledValue, scaledValue, 1)
        self.disp.show()
        
    def showWaitTime(self, toWait):
        """ The method shows the wait time until the next data refresh

            Parameters
            ----------
            toWait : int
                the wait time
        """
        
        # clean the time area
        self.disp.vline(time_x, time_start_y, time_max_y - time_start_y + 1, 0)
        # show the time bar
        value = max(time_min, min(time_max, toWait))
        scaledValue = int(value / time_scale)
        self.disp.vline(time_x, time_max_y - scaledValue, scaledValue, 1)
        self.disp.show()

    def showText(self, text):
        self.disp.fill(0)
        self.disp.text(text, 0, 0)
        self.disp.show()
        
    def clean(self):
        self.disp.fill(0)
        self.disp.show()