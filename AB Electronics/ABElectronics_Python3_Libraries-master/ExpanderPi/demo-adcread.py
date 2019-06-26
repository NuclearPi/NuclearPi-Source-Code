#!/usr/bin/python3

from ABE_ExpanderPi import ADC
import time
import os

"""
================================================
ABElectronics Expander Pi | ADC Read Demo
Version 1.0 Created 29/03/2015

run with: python3 demo-adcread.py
================================================

this demo reads the voltage from all channels on the ADC inputs
"""
def cls():
    os.system('cls' if os.name=='nt' else 'clear')

adc = ADC()  # create an instance of the ADC

# set the reference voltage.  this should be set to the exact voltage
# measured on the Expander Pi Vref pin.
adc.set_adc_refvoltage(4.096)

clear = lambda: os.system('cls')

while True:
    cls()
    # read the voltage from the 8 channels in single ended mode and display on the screen
    print ("Channel 1: ", adc.read_adc_voltage(1, 0))
    print ("Channel 2: ", adc.read_adc_voltage(2, 0))
    print ("Channel 3: ", adc.read_adc_voltage(3, 0))
    print ("Channel 4: ", adc.read_adc_voltage(4, 0))
    print ("Channel 5: ", adc.read_adc_voltage(5, 0))
    print ("Channel 6: ", adc.read_adc_voltage(6, 0))
    print ("Channel 7: ", adc.read_adc_voltage(7, 0))
    print ("Channel 8: ", adc.read_adc_voltage(8, 0))
    time.sleep(0.1)
