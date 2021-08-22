# rainradar
(in development)

Rain Radar (German: Regenradar)  displays the rain forecast  on a 32x8 led matrix.
It shows the intencity of the rain for the next 2 hours as LED bars one for every 5 minutes.


# common
The Rain Radar is a combination of:
- a ESP8266 microcontroller
- a chain of 4 MAX7219 8x8 LED matrices
- an online service providing the rain forecast in mm/h for a geographic coordinate

# setup
(draft)
- connect ESP8266 and MAX7219 accroding to https://github.com/mcauser/micropython-max7219
- install Python on the PC
- flash the MicroPython image to the ESP 8266 as described in https://docs.micropython.org/en/latest/esp8266/tutorial/intro.html
  - pip install esptool
  - esptool.py erase_flash
  - esptool.py  write_flash --flash_size=detect 0  ~/Downloads/esp8266/micropython/esp8266-20210618-v1.16.bin
- install the tool to copy the files from to ESP8266
  - pip install adafruit-ampy
  - ampy --port COM3 ls
- download the max7219.py module from  https://github.com/mcauser/micropython-max7219
- upload the max7219 module to the ESP8266
  - ampy --port COM3 mkdir lib
  - ampy --port COM3 put ~/Downloads/esp8266/micropython/max7219.py lib/max7219.py
  - ampy --port COM3 ls lib

