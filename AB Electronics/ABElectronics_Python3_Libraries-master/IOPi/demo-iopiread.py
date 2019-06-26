#!/usr/bin/python3

from ABE_helpers import ABEHelpers
from ABE_IoPi import IoPi
import time
import os

"""
================================================
ABElectronics IO Pi 32-Channel Port Expander - Input Read Demo
Version 1.0 Created 29/02/2015

Requires python 3 smbus to be installed
run with: python3 demo-iopiread.py
================================================

This example reads the first 8 pins of bus 1 on the IO Pi board.  The
internal pull-up resistors are enabled so each pin will read as 1 unless
the pin is connected to ground.

Initialise the IOPi device using the default addresses, you will need to
change the addresses if you have changed the jumpers on the IO Pi
"""
i2c_helper = ABEHelpers()
i2c_bus = i2c_helper.get_smbus()

bus = IoPi(i2c_bus, 0x20)

# We will read the inputs 1 to 8 from bus 2 so set port 0 to be inputs and
# enable the internal pull-up resistors
bus.set_port_direction(0, 0xFF)
bus.set_port_pullups(0, 0xFF)

while True:
    # clear the console
    os.system('clear')

    # read the pins 1 to 8 and print the results
    print ('Pin 1: ' + str(bus.read_pin(1)))
    print ('Pin 2: ' + str(bus.read_pin(2)))
    print ('Pin 3: ' + str(bus.read_pin(3)))
    print ('Pin 4: ' + str(bus.read_pin(4)))
    print ('Pin 5: ' + str(bus.read_pin(5)))
    print ('Pin 6: ' + str(bus.read_pin(6)))
    print ('Pin 7: ' + str(bus.read_pin(7)))
    print ('Pin 8: ' + str(bus.read_pin(8)))

    # wait 0.5 seconds before reading the pins again
    time.sleep(0.1)
