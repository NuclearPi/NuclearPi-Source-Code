AB Electronics UK IO Pi Python 3 Library
=====

Python 3 Library to use with IO Pi Raspberry Pi expansion board from https://www.abelectronics.co.uk

Install
====
To download to your Raspberry Pi type in terminal: 

```
git clone https://github.com/abelectronicsuk/ABElectronics_Python3_Libraries.git
```

The IO Pi library is located in the IOPi directory

The library requires i2c to be enabled and python-smbus to be installed.

Follow the tutorial at [https://www.abelectronics.co.uk/i2c-raspbian-wheezy/info.aspx](https://www.abelectronics.co.uk/i2c-raspbian-wheezy/info.aspx) to enable i2c and install python-smbus for python 3.

Add the location where you downloaded the python libraries into PYTHONPATH e.g. download location is Desktop
```
export PYTHONPATH=${PYTHONPATH}:~/Desktop/ABElectronics_Python3_Libraries/IOPi/
```

The example python files in /ABElectronics_Python3_Libraries/IOPi/ will now run from the terminal.


Functions:
----------

```
set_pin_direction(pin, direction):
```
Sets the IO direction for an individual pin  
**Parameters:** pin - 1 to 16, direction - 1 = input, 0 = output  
**Returns:** null

```
set_port_direction(port, direction): 
```
Sets the IO direction for the specified IO port  
**Parameters:** port - 0 = pins 1 to 8, port 1 = pins 9 to 16, direction - 1 = input, 0 = output  
**Returns:** null
```
set_port_pullups(self, port, value)
```
Set the internal 100K pull-up resistors for the selected IO port  
**Parameters:** port - 1 to 16, value: 1 = Enabled, 0 = Disabled  
**Returns:** null

```
write_pin(pin, value)
```
Write to an individual pin 1 - 16  
**Parameters:** pin - 1 to 16, value - 1 = Enabled, 0 = Disabled
**Returns:** null
```
write_port(self, port, value)
```
Write to all pins on the selected port  
**Parameters:** port - 0 = pins 1 to 8, port 1 = pins 9 to 16, value -  number between 0 and 255 or 0x00 and 0xFF  
**Returns:** null
```
read_pin(pin)
```
Read the value of an individual pin 1 - 16   
**Parameters:** pin: 1 to 16  
**Returns:** 0 = logic level low, 1 = logic level high
```
read_port(port)
```
Read all pins on the selected port  
**Parameters:** port - 0 = pins 1 to 8, port 1 = pins 9 to 16  
**Returns:** number between 0 and 255 or 0x00 and 0xFF
```
invert_port(port, polarity)
```
Invert the polarity of the pins on a selected port  
**Parameters:** port - 0 = pins 1 to 8, port 1 = pins 9 to 16, polarity - 0 = same logic state of the input pin, 1 = inverted logic state of the input pin  
**Returns:** null

```
invert_pin(pin, polarity)
```
Invert the polarity of the selected pin  
**Parameters:** pin - 1 to 16, polarity - 0 = same logic state of the input pin, 1 = inverted logic state of the input pin
**Returns:** null
```
mirror_interrupts(value)
```
Mirror Interrupts  
**Parameters:** value - 1 = The INT pins are internally connected, 0 = The INT pins are not connected. INTA is associated with PortA and INTB is associated with PortB  
**Returns:** null
```
set_interrupt_type(port, value)
```
Sets the type of interrupt for each pin on the selected port  
**Parameters:** port 0 = pins 1 to 8, port 1 = pins 9 to 16, value: 1 = interrupt is fired when the pin matches the default value, 0 = the interrupt is fired on state change  
**Returns:** null
```
set_interrupt_defaults(port, value)
```
These bits set the compare value for pins configured for interrupt-on-change on the selected port.  
If the associated pin level is the opposite from the register bit, an interrupt occurs.    
**Parameters:** port 0 = pins 1 to 8, port 1 = pins 9 to 16, value: compare value  
**Returns:** null
```
set_interrupt_on_port(port, value)
```
Enable interrupts for the pins on the selected port  
**Parameters:** port 0 = pins 1 to 8, port 1 = pins 9 to 16, value: number between 0 and 255 or 0x00 and 0xFF  
**Returns:** null

```
set_interrupt_on_pin(pin, value)
```
Enable interrupts for the selected pin  
**Parameters:** pin - 1 to 16, value - 0 = interrupt disabled, 1 = interrupt enabled  
**Returns:** null

```
read_interrupt_status(port)
```
Read the interrupt status for the pins on the selected port  
**Parameters:** port 0 = pins 1 to 8, port 1 = pins 9 to 16  
**Returns:** status

```
read_interrupt_capture(port)
```
Read the value from the selected port at the time of the last interrupt trigger  
**Parameters:** port 0 = pins 1 to 8, port 1 = pins 9 to 16  
**Returns:** status
```
reset_interrupts()
```
Set the interrupts A and B to 0  
**Parameters:** null  
**Returns:** null
Usage
====
To use the IO Pi library in your code you must first import the library:
```
from ABE_IOPi import IOPI
```
Now import the helper class
```
from ABE_helpers import ABEHelpers
```
Next you must initialise the IO object with the smbus object using the helpers:

```
i2c_helper = ABEHelpers()
bus = i2c_helper.get_smbus()
bus1 = IOPI(bus,0x20)
```

We will read the inputs 1 to 8 from bus 2 so set port 0 to be inputs and enable the internal pull-up resistors 

```
bus1.set_port_direction(0, 0xFF)
bus1.set_port_pullups(0, 0xFF)
```

You can now read the pin 1 with:
```
print 'Pin 1: ' + str(bus1.read_pin(1))
```
