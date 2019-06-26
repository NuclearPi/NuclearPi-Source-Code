AB Electronics UK RTC Pi Python 3 Library
=====

Python 3 Library to use with RTC Pi Raspberry Pi real-time clock boards from https://www.abelectronics.co.uk

Install
====

To download to your Raspberry Pi type in terminal: 

```
git clone https://github.com/abelectronicsuk/ABElectronics_Python3_Libraries.git
```
The RTC Pi library is located in the RTCPi directory

Add the location where you downloaded the python libraries into PYTHONPATH e.g. download location is Desktop
```
export PYTHONPATH=${PYTHONPATH}:~/Desktop/ABElectronics_Python_Libraries/RTCPi/
```

The library requires i2c to be enabled and python-smbus to be installed.

Follow the tutorial at [https://www.abelectronics.co.uk/i2c-raspbian-wheezy/info.aspx](https://www.abelectronics.co.uk/i2c-raspbian-wheezy/info.aspx) to enable i2c and install python-smbus for python 3.

The example python files in /ABElectronics_Python3_Libraries/RTCPi/ will now run from the terminal.

Functions:
----------

```
set_date(date) 
```
Set the date and time on the RTC in ISO 8601 format - YYYY-MM-DDTHH:MM:SS   
**Parameters:** date   
**Returns:** null

```
read_date() 
```
Returns the date from the RTC in ISO 8601 format - YYYY-MM-DDTHH:MM:SS   
**Returns:** date


```
enable_output() 
```
Enable the square-wave output on the SQW pin.  
**Returns:** null

```
disable_output()
```
Disable the square-wave output on the SQW pin.   
**Returns:** null

```
set_frequency()
```
Set the frequency for the square-wave output on the SQW pin.   
**Parameters:** frequency - options are: 1 = 1Hz, 2 = 4.096KHz, 3 = 8.192KHz, 4 = 32.768KHz   
**Returns:** null

Usage
====

To use the RTC Pi library in your code you must first import the library:
```
from ABE_RTCPi import RTC
```

Now import the helper class
```
from ABE_helpers import ABEHelpers
```
Next you must initialise the RTC object with the smbus object using the helpers:

```
i2c_helper = ABEHelpers()
bus = i2c_helper.get_smbus()
rtc = RTC(bus)
```
Set the current time in ISO 8601 format:
```
rtc.set_date("2013-04-23T12:32:11")
```
Enable the square-wave output at 8.192KHz on the SQW pin:
```
rtc.set_frequency(3)
rtc.enable_output()
```
Read the current date and time from the RTC at 1 second intervals:
```
while (True):
  print rtc.read_date()
  time.sleep(1)
```
