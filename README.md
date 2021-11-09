# rainradar

Rain Radar (German: Regenradar)  displays the rain forecast on a 32x8 led matrix.
It shows the intensity of the rain for the next 2 hours with 5 minutes resolution 
and the intensity of the rain for the 6 hours (following the 2 hours) with 1 hour resolution.

![picture](doc/rainradar.jpg)

# common
The Rain Radar is a combination of:
- an ESP32 micro controller
- a chain of four MAX7219 8x8 LED matrices
- an online service providing the weather forecast by German postal index, https://morgenwirdes.de/api/

The project is inspired by the project from the German Make Magazine https://github.com/MakeMagazinDE/LED-Laufschrift

# manual

See [User Manual](doc/manual/MANUAL.md)

# assembly

See [Assembly](docs/assembly/ASSEMBLY.md)
# setup

- install Python on the PC
- flash the MicroPython image on the ESP32 as described in https://docs.micropython.org/en/latest/esp32/tutorial/intro.html
  - `pip install esptool`
  - `esptool.py erase_flash`
  - `esptool.py  write_flash -z 0x1000  ~/Downloads/esp32/micropython/esp32-20210902-v1.17.bin`
- install the tool to copy the files to ESP32
  - `pip install adafruit-ampy`
  - `ampy --port COM4 ls`
- download the `max7219.py` module from  https://github.com/mcauser/micropython-max7219
- upload the max7219 module to the ESP32
  - `ampy --port COM4 mkdir lib`
  - `ampy --port COM4 put ~/Downloads/esp32/micropython/max7219.py lib/max7219.py`
  - `ampy --port COM4 ls lib`
- download the rainradar code from this project
- upload the rainradar code (i.e. the python modules *.py) to the ESP32
  - `ampy --port COM4 put ~/Downloads/esp32/rainradar/rainradar/`
  - `ampy --port COM4 ls`
- restart ESP32

