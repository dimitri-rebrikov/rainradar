import time
from display import WeatherDisplay
from radar import Radar
import wifi

wifi.connect('xxxxxx','xxxxxxx')

disp = WeatherDisplay()
radar = Radar(90402)

while True:
    radarData = radar.getData()
    disp.showRadarData(radarData)
    #disp.showRadarData([-10, 0, 10, 15, 20, 25, 30, 40, 50, 60, 70, 80, 70, 60, 50, 40, 30, 20, 10, 0, 30, 40, 80, 20, 30, 50, 10, -10, 0, 10, 20, 30, 40, 50, 60, 70, 80, 70, 60, 50, 40, 30, 20, 10, 0, 30, 40, 80, 20, 30, 50, 10])

    for i in range(5, 0, -1):
        for j in range(30):
            disp.showWaitTime(i)
            time.sleep(1)
            disp.showWaitTime(i-1)
            time.sleep(1)

