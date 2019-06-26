#!/usr/bin/python3

from ABE_ExpanderPi import DAC
import time

"""
================================================
ABElectronics Expander Pi | DAC Write Demo
Version 1.0 Created 29/03/2015

run with: python3 demo-dacwrite.py
================================================

this demo will generate a 1.5V p-p square wave at 1Hz on channel 1
"""

dac = DAC()

while True:
    dac.set_dac_voltage(1, 1.5)  # set the voltage on channel 1 to 1.5V
    time.sleep(0.5)  # wait 0.5 seconds
    dac.set_dac_voltage(1, 0)  # set the voltage on channel 1 to 0V
    time.sleep(0.5)  # wait 0.5 seconds
