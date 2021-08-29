import time
from display import Display
from radar import Radar
import wifi
from config import Config
from exception import RainradarException
import rain

while True:
    disp = Display()
    try:
        cfg = Config()
        plz = cfg.getPlz()
        disp.showText(plz, 2)
        wifi.connect(cfg.getSsid(), cfg.getPassword())
        radar = Radar(plz)
        while True:
            levelList = rain.mmListToLevelList(radar.getMmList())
            disp.showRainLevels(levelList)
            for i in range(5, 0, -1):
                for j in range(30):
                    disp.showWaitTime(i)
                    time.sleep(1)
                    disp.showWaitTime(i-1)
                    time.sleep(1)

    except RainradarException as exp:
        disp.showText(str(exp), 2)
