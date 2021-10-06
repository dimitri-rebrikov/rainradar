# Manual for the Rainradar

## Controls and Connections

![](controls.jpg)

1. Display
2. Power LED
3. Configuration Button
4. Micro USB Socket 

## Operational Mode

In this mode the Rainradar displays the short rain forecast in the left part of the display and middle term rain forecast in the right part.

The short term forecast show the rain levels for the coming 2 hours with the resolution of 5 min.

The middle term forecast show the rain levels for the 6 hours after the 2 hours of the short term forecast. The resolution is 1 hour.

Additional there is a blinking LED on the left edge of the display representing the liveness of the device. The distance of this LED to the upper corner of the display additionally represent the amount of time (in minutes) to the next refresh of the rain levels

**Remark**
During the start (i.e. after powering of the Rainradar over the Micro USB connection) the Rainradar shows for some seconds the Postal Index it configured to provide the forecast for.

### Rain Levels

The rain levels presented as a bar diagram. The height of the bar (i.e. the number of the shining LED's in the row) visualize the strength of the rain in the corresponding time period.

The following table decodes the number of the LED's in the bar into the corresponding rain level:

| Number of the LED's | Rain Level in Text | Rain Level in mm/m2 |
|---------------------|--------------------|---------------------|
| 1 | No Rain | < 0.1 |
| 2 | Very Light Rain | 0.1 to 1.2 |
| 3 | Light Rain | 1.2 to 2.5 |
| 4 | Light to Moderate Rain | 2.5 to 5.5 |
| 5 | Moderate Rain | 5.5 to 10 |
| 6 | Moderate to Heavy Rain | 10 to 25 |
| 7 | Heavy Rain | 25 to 50 |
| 8 | Very Heavy Rain | from 50 |

### Example

![](example.jpg)

This example represent the following situation:

**Short Therm Part on the Left**

- in the next 5 minutes there will be Light to Moderate rain (the first row with 4 LED's)
- after that there will be Very Light and Light Rain (the next 7 LED rows with 2 or 3 LED's in each) for 35 min (7 x 5 = 35)
- after that there will be no Rain for 20 minutes (the 4 LED rows with only one LED)
- after that (so ca. after 1 hour from now) there will be Light to Moderate Rain for ca. half of an hour which then will decline.

**Middle Therm Part on the Right**

For the time period starting with 3 to 8 hours from now there will be probably Very Light Rain.

### Errors

In case of application errors during the Operational Mode they are shown for some seconds on the display. After this time the application restarts.

The following table show know errors:

| Error on Display | Meaning | Possible Issue | Possible solution |
|------------------|---------|----------------|-------------------|
| **ERR WIFI** | The Rainradar could not connect to the WiFi network | No connection to the WiFi router | Fix the connection to the router, see Configuration Mode |
| **ERR NTP** | The Rainradar could not connect to the NTP server to synchronize its clock |  No connection to the internet | Fix connection to the internet in the WiFi router |
| **ERR GET RADAR** or **ERR GET RAIN**| The Rainradar could not get the short therm rain information from the server. | No connection to the internet | see above |
|  |  | The server providing the radar information is broken/down | The rainradar uses the [morgenwirdes](https://morgenwirdes.de/api/) server to get the information. Try to visit the site to get more information |
| **ERR JSON RADAR** or **ERR JSON RAIN**| The Rainradar could not parse the information provided by the server | The server providing the radar information is broken | see above |

In case you suspect the issues in the application itself you can raise an issue ticket in https://github.com/dimitri-rebrikov/rainradar/issues

## Configuration Mode

The configuration mode allows to change the parameters necessary for the Operation Mode:

- the credentials (SSID and password) of the WiFi network the Rainradar shall connect for
- the German postal index code (PLZ) the Rainradar shall provide the rain forecast for

During the initial start (i.e. if there is no configuration) the Rainradar will automatically switch into the Configuration Mode.

To switch into configuration mode any time later you shall press the Configuration Button trough the hole in the lid. Please use an thin non-metal stick for this, for example a toothpick. The Button will make a haptic noticeable click. One click is enough.

After switching into the Configuration Mode the Rainradar will show "CONF" on the display.

![](conf.jpg)

To configure the Rainradar you shall directly connect to it over its WiFi.

### Connect to Rainradar over WiFi

In the Configuration Mode the Rainradar starts ist own WiFi Access Point.
Open your WiFi configuration dialog where the WiFi network with the name "rainradar" will appear.

<img src="select_rainradar.jpg" height="600">

You shall connect to this Access Point:
- SSID: rainradar
- Password: rainradar2021

After successful connection you might get warning that there is no connection ot internet. This is ok, as now you connected exclusively only to the Rainradar.

Now open the Address [http://192.168.41.1](http://192.168.41.1) in the Web Browser and the Configuration Page shall be displayed

### Configuration Page 

<img src="config_page.jpg" height="600">

In the configuration page you shall provide the Name and the Password of the WiFi network the Rainradar shall use to connect to the internet. It is probably just your WiFi you use for your devices at home. 

The chapter "Available WiFi's" helps your with the names of the WiFi Networks available.

Additionally you shall provide the German Postal Index (PLZ) of the location the Rainradar shall display the rain forecast for. It is probably just you postal index.

After the 3 configuration parameters are provided hit the "Save changes" button.

The Rainradar will test the WiFi parameter and provide the result in the "WiFi Status" chapter. If the status is "Not connected" the issues might be the following:
| Issue | Solution |
|-------|----------|
| Wrong WiFi name or password | Correct the data and hit "Save changes" again |
| The WiFi network does not allow connection of the "unknown" devices | Configure your WiFi router accordingly. i.e. Either remove the protection or add the Rainradar to the list of the know devices. After that hit the "Retest WiFi Connection" button for a new try |
| The WiFi network signal is to weak | Search a location near to the WiFi router and hit the "Retest WiFi Connection" button for a new try |

**Attention:** there is no check for the right Postal Index so ensure you provide correct value. Otherwise the rain forecast will be wrong.

After successful configuration you can exit the config mode by hitting of the "Exit Config" button. The Rainradar will stop its Access Point, so the connection to the Rainradar will be lost and your device will probably automatically connect to your home network again.

The Rainradar will switch back to the Operational Mode