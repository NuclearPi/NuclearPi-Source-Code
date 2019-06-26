#!/usr/bin/python3
"""
================================================
ABElectronics IO Pi 32-Channel Port Expander - Tutorial 1a
Version 1.0 Created 29/02/2015

Requires python 3 smbus to be installed
run with: python3 tutorial1a.py
================================================

This example uses the write_port method to count in binary using 8 LEDs
"""
from ABE_helpers import ABEHelpers
from ABE_IoPi import IoPi
import time

i2c_helper = ABEHelpers()
i2c_bus = i2c_helper.get_smbus()

bus = IoPi(i2c_bus, 0x20)

bus.set_port_direction(0, 0x00)
bus.write_port(0, 0x00)

while True:
    for x in range(0, 255):
        bus.write_port(0, x)
        time.sleep(0.5)

        bus.write_port(0, 0x00)
