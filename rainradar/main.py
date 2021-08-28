import time
from display import WeatherDisplay
from radar import Radar
import wifi
from config import Config
from exception import RainradarException

while True:
    disp = WeatherDisplay()
    disp.showText("STRT")
    try:
        cfg = Config()
        wifi.connect(cfg.getSsid(), cfg.getPassword())
        radar = Radar(cfg.getPlz())

        while True:
            radarData = radar.getData()
            disp.clean()
            disp.showRadarData(radarData)
            for i in range(5, 0, -1):
                for j in range(30):
                    disp.showWaitTime(i)
                    time.sleep(1)
                    disp.showWaitTime(i-1)
                    time.sleep(1)

    except RainradarException as exp:
        disp.showText(str(exp))
        time.sleep(5)
