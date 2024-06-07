# rainradar

Rain Radar (German: Regenradar)  displays the rain forecast on a 32x8 led matrix.
It shows the intensity of the rain for the next 2 hours with 5 minutes resolution 
and the intensity of the rain for the 6 hours (following the 2 hours) with 1 hour resolution.

![picture](doc/rainradar.jpg)

# common
The Rain Radar consist of:

Frontend Device:
- an ESP32 micro controller
- a chain of four MAX7219 8x8 LED matrices
- source code implemented in MycroPython accessing to the backend and visualising the rain forecast data on the matrix

Backend/Online Services:
- AWS Lambda collecting rain radar data (Radolan RV) from the DWD (German Federal Weather Service) for all Gemran postal indexes (PLZ's)
- AWA Lambda collecting rain forecast data (Mosmix) from the DWD for all German postal indexes
- AWD Lambda providing rain radar and rain forecast data on a HTTP GET request with a German postal index as query parameter

The project is inspired by the project from the German Make Magazine https://github.com/MakeMagazinDE/LED-Laufschrift

# user manual for the device

See [User Manual](doc/manual/MANUAL.md)

# assembly of the device

See [Assembly](doc/assembly/ASSEMBLY.md)
# setup of the device

- install Silicon Labs CP210x VCP driver from silabs.com so your PC can communicate with the ESP32 
- install Python 3.x as the software used below depends on it
- flash the MicroPython image on the ESP32 as described in https://docs.micropython.org/en/latest/esp32/tutorial/intro.html
  - `pip3 install esptool`
  - `esptool.py erase_flash`
  - `esptool.py  write_flash -z 0x1000  ~/Downloads/esp32/micropython/esp32-20210902-v1.17.bin` (assuming you downloaded the image into %HOMEPATH%/Downloads/esp32/micropython)
- install the tool to copy the files to ESP32
  - `pip3 install adafruit-ampy`
  - `ampy --port COM4 ls` (Change COM4 to the port number valid on your PC. Look into the device manager for this. If ampy hangs try to add the delay paramter to the command, i.e. `ampy --port COM4 -d 1 ls`)
- download the `max7219.py` module from  https://github.com/mcauser/micropython-max7219
- upload the max7219 module to the ESP32
  - `ampy --port COM4 mkdir lib`
  - `ampy --port COM4 put ~/Downloads/esp32/micropython/max7219.py lib/max7219.py` (assuming you downloaded the module into %HOMEPATH%/Downloads/esp32/micropython)
  - `ampy --port COM4 ls lib`
- download this project (i.e. https://github.com/dimitri-rebrikov/rainradar)
- upload the rainradar code (i.e. the python modules *.py) to the ESP32
  - `ampy --port COM4 put ~/Downloads/esp32/rainradar/rainradar/ .` (assuming you downloaded the project into %HOMEPATH%/Downloads/esp32/rainradar)
  - `ampy --port COM4 ls`
- restart ESP32 by disconnecting/connecting the power supply (i.e. USB)

# backend

See [Backend](aws-backend/BACKEND.md)