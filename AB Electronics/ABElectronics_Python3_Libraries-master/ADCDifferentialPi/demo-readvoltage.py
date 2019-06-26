#!/usr/bin/python3

from ABE_ADCDifferentialPi import ADCDifferentialPi
from ABE_helpers import ABEHelpers
import time
import os

"""
================================================
ABElectronics ADC Differential Pi 8-Channel ADC demo
Version 1.0 Created 30/09/2015

Requires python 3 smbus to be installed
run with: python3 demo-read_voltage.py
================================================


Initialise the ADC device using the default addresses and sample rate, change this value if you have changed the address selection jumpers
Sample rate can be 12,14, 16 or 18
"""

i2c_helper = ABEHelpers()
bus = i2c_helper.get_smbus()
adc = ADCDifferentialPi(bus, 0x68, 0x69, 18)

while (True):

    # clear the console
    os.system('clear')

    # read from adc channels and print to screen
    print ("Channel 1: %02f" % adc.read_voltage(1))
    print ("Channel 2: %02f" % adc.read_voltage(2))
    print ("Channel 3: %02f" % adc.read_voltage(3))
    print ("Channel 4: %02f" % adc.read_voltage(4))
    print ("Channel 5: %02f" % adc.read_voltage(5))
    print ("Channel 6: %02f" % adc.read_voltage(6))
    print ("Channel 7: %02f" % adc.read_voltage(7))
    print ("Channel 8: %02f" % adc.read_voltage(8))

    # wait 0.5 seconds before reading the pins again
    time.sleep(0.5)
