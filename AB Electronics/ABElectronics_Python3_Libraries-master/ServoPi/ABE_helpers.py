#!/usr/bin/python3
try:
    import smbus
except ImportError:
    raise ImportError("python-smbus not found Install with 'sudo apt-get install python3-smbus'")
import re

"""
================================================
ABElectronics Python Helper Functions
Version 1.0 Created 29/02/2015
Python 3 only
Requires python 3 smbus to be installed.  For more information
about enabling i2c and installing smbus visit
https://www.abelectronics.co.uk/i2c-raspbian-wheezy/info.aspx
================================================
"""


class ABEHelpers:
    
    def get_smbus(self):
        # detect i2C port number and assign to i2c_bus
        i2c_bus = 0
        for line in open('/proc/cpuinfo').readlines():
            m = re.match('(.*?)\s*:\s*(.*)', line)
            if m:
                (name, value) = (m.group(1), m.group(2))
                if name == "Revision":
                    if value[-4:] in ('0002', '0003'):
                        i2c_bus = 0
                    else:
                        i2c_bus = 1
                    break
        try:        
            return smbus.SMBus(i2c_bus)
        except IOError:
                print ("Could not open the i2c bus.")
                print ("Please check that i2c is enabled and python-smbus and i2c-tools are installed.")
                print ("Visit https://www.abelectronics.co.uk/i2c-raspbian-wheezy/info.aspx for more information.")    