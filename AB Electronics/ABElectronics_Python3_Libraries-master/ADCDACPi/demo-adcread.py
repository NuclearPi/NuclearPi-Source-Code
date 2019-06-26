#!/usr/bin/python3

from ABE_ADCDACPi import ADCDACPi
import time

"""
================================================
ABElectronics ADCDAC Pi 2-Channel ADC, 2-Channel DAC | ADC Read Demo
Version 1.0 Created 29/02/2015

run with: python3 demo-adcread.py
================================================

this demo reads the voltage from channel 1 on the ADC inputs
"""

adcdac = ADCDACPi()  # create an instance of ADCDACPi

# set the reference voltage.  this should be set to the exact voltage
# measured on the raspberry pi 3.3V rail.
adcdac.set_adc_refvoltage(3.3)

while True:
    # read the voltage from channel 1 in single ended mode and display on the screen
    print (adcdac.read_adc_voltage(1, 0))
    time.sleep(0.5)
