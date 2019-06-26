#!/usr/bin/python
import datetime
import re

"""
================================================
ABElectronics RTC Pi Real-time clock
Version 1.0 Created 29/02/2015

Requires python 3 smbus to be installed

================================================
"""


class RTC:
    # Define registers values from datasheet
    SECONDS = 0x00
    MINUTES = 0x01
    HOURS = 0x02
    DAYOFWEEK = 0x03
    DAY = 0x04
    MONTH = 0x05
    YEAR = 0x06
    CONTROL = 0x07

    # variables
    __rtcAddress = 0x68  # I2C address
    # initial configuration - square wave and output disabled, frequency set
    # to 32.768KHz.
    __config = 0x03
    # the DS1307 does not store the current century so that has to be added on
    # manually.
    __century = 2000

    global _bus

    # local methods

    def __init__(self, bus):
        self._bus = bus
        self._bus.write_byte_data(self.__rtcAddress, self.CONTROL, self.__config)
        return

    def __bcd_to_dec(self,bcd):
        """
        internal method for converting BCD formatted number to decimal
        """
        dec = 0
        for a in (bcd >> 4, bcd):
            for b in (1, 2, 4 ,8):
                if a & 1:
                    dec += b
                a >>= 1
            dec *= 10
        return dec / 10    
    
    def __dec_to_bcd(self,dec):
        """
        internal method for converting decimal formatted number to BCD
        """
        bcd = 0
        for a in (dec // 10, dec % 10):
            for b in (8, 4, 2, 1):
                if a >= b:
                    bcd += 1
                    a -= b
                bcd <<= 1
        return bcd >> 1

    def __get_century(self, val):
        if len(val) > 2:
            y = val[0] + val[1]
            self.__century = int(y) * 100
        return

    def __updatebyte(self, byte, bit, value):
        """
        internal method for setting the value of a single bit within a byte
        """

        if value == 0:
            return byte & ~(1 << bit)
        elif value == 1:
            return byte | (1 << bit)

    # public methods
    def set_date(self, date):
        """
        set the date and time on the RTC
        date must be in ISO 8601 format - YYYY-MM-DDTHH:MM:SS
        """

        d = datetime.datetime.strptime(date, "%Y-%m-%dT%H:%M:%S")
        self.__get_century(date)
        self._bus.write_byte_data(
            self.__rtcAddress,
            self.SECONDS,
            self.__dec_to_bcd(
                d.second))
        self._bus.write_byte_data(
            self.__rtcAddress,
            self.MINUTES,
            self.__dec_to_bcd(
                d.minute))
        self._bus.write_byte_data(
            self.__rtcAddress,
            self.HOURS,
            self.__dec_to_bcd(
                d.hour))
        self._bus.write_byte_data(
            self.__rtcAddress,
            self.DAYOFWEEK,
            self.__dec_to_bcd(
                d.weekday()))
        self._bus.write_byte_data(
            self.__rtcAddress,
            self.DAY,
            self.__dec_to_bcd(
                d.day))
        self._bus.write_byte_data(
            self.__rtcAddress,
            self.MONTH,
            self.__dec_to_bcd(
                d.month))
        self._bus.write_byte_data(
            self.__rtcAddress,
            self.YEAR,
            self.__dec_to_bcd(
                d.year -
                self.__century))
        return

    def read_date(self):
        """
        read the date and time from the RTC in ISO 8601 format -
        YYYY-MM-DDTHH:MM:SS
        """

        seconds, minutes, hours, dayofweek, day, month,\
            year = self._bus.read_i2c_block_data(self.__rtcAddress, 0, 7)
        date = (
            "%02d-%02d-%02dT%02d:%02d:%02d " %
            (self.__bcd_to_dec(year) +
             self.__century,
             self.__bcd_to_dec(month),
             self.__bcd_to_dec(day),
             self.__bcd_to_dec(hours),
             self.__bcd_to_dec(minutes),
             self.__bcd_to_dec(seconds)))
        return date

    def enable_output(self):
        """
        Enable the output pin
        """

        self.__config = self.__updatebyte(self.__config, 7, 1)
        self.__config = self.__updatebyte(self.__config, 4, 1)
        self._bus.write_byte_data(self.__rtcAddress, self.CONTROL, self.__config)
        return

    def disable_output(self):
        """
        Disable the output pin
        """

        self.__config = self.__updatebyte(self.__config, 7, 0)
        self.__config = self.__updatebyte(self.__config, 4, 0)
        self._bus.write_byte_data(self.__rtcAddress, self.CONTROL, self.__config)
        return

    def set_frequency(self, frequency):
        """
        set the frequency of the output pin square-wave
        options are: 1 = 1Hz, 2 = 4.096KHz, 3 = 8.192KHz, 4 = 32.768KHz
        """

        if frequency == 1:
            self.__config = self.__updatebyte(self.__config, 0, 0)
            self.__config = self.__updatebyte(self.__config, 1, 0)
        if frequency == 2:
            self.__config = self.__updatebyte(self.__config, 0, 1)
            self.__config = self.__updatebyte(self.__config, 1, 0)
        if frequency == 3:
            self.__config = self.__updatebyte(self.__config, 0, 0)
            self.__config = self.__updatebyte(self.__config, 1, 1)
        if frequency == 4:
            self.__config = self.__updatebyte(self.__config, 0, 1)
            self.__config = self.__updatebyte(self.__config, 1, 1)
        self._bus.write_byte_data(self.__rtcAddress, self.CONTROL, self.__config)
        return
