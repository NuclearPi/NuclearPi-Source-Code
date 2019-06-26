#!/usr/bin/python3

from ABE_RTCPi import RTC
from ABE_helpers import ABEHelpers
import time

"""
================================================
ABElectronics RTC Pi real-time clock | Set Time Demo
Version 1.0 Created 29/02/2015

Requires python 3 smbus to be installed

run with: python3 demo-rtcsettime.py
================================================

This demo shows how to set the time on the RTC Pi and then read the
current time at 1 second intervals
"""

i2c_helper = ABEHelpers()
bus = i2c_helper.get_smbus()
rtc = RTC(bus)  # create a new instance of the RTC class


# set the date using ISO 8601 format - YYYY-MM-DDTHH:MM:SS
rtc.set_date("2013-04-23T12:32:11")

while True:
    # read the date from the RTC in ISO 8601 format and print it to the screen
    print (rtc.read_date())
    time.sleep(1)  # wait 1 second
