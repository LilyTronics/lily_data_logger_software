"""
Serial port interface.
"""

import time
import serial
import wx

from src.models.interfaces.interface import Interface
from src.models.list_serial_ports import get_available_serial_ports


class SerialPortInterface(Interface):

    NAME = "Serial port"
    DEFAULT_TIMEOUT = 3

    _TOGGLE_INTERVAL = 0.005

    _BAUD_RATES = [1200, 1800, 2400, 4800, 9600, 14400, 19200, 28800, 31250, 38400, 57600,
                   76800, 115200, 128000, 230400, 250000, 256000, 460800, 500000, 576000, 921600,
                   1000000]
    _DEFAULT_BAUD_RATE = 19200
    _PARITY_VALUES = {
        "None": serial.PARITY_NONE,
        "Odd": serial.PARITY_ODD,
        "Even": serial.PARITY_EVEN,
        "Mark": serial.PARITY_MARK,
        "Space": serial.PARITY_SPACE
    }
    _DEFAULT_PARITY = "None"
    _STOP_BITS = [serial.STOPBITS_ONE, serial.STOPBITS_ONE_POINT_FIVE, serial.STOPBITS_TWO]
    _DEFAULT_STOP_BITS = serial.STOPBITS_ONE
    _DATA_BITS = [serial.FIVEBITS, serial.SIXBITS, serial.SEVENBITS, serial.EIGHTBITS]
    _DEFAULT_DATA_BITS = serial.EIGHTBITS

    # pylint: disable=too-many-arguments
    def __init__(self, serial_port, baud_rate=_DEFAULT_BAUD_RATE, parity=_DEFAULT_PARITY,
                 stop_bits=_DEFAULT_STOP_BITS, data_bits=_DEFAULT_DATA_BITS,
                 rx_timeout=DEFAULT_TIMEOUT, tx_timeout=0):
        params_to_match = {
            "serial_port": serial_port
        }
        super().__init__(params_to_match)
        if tx_timeout == 0:
            tx_timeout = rx_timeout
        self._rx_time_out = rx_timeout
        self._serial = serial.Serial(serial_port, baudrate=int(baud_rate),
                                     parity=self._PARITY_VALUES[parity], stopbits=float(stop_bits),
                                     bytesize=int(data_bits), write_timeout=tx_timeout)

    def toggle_dtr(self):
        for value in (True, False, True):
            self._serial.dtr = value
            time.sleep(self._TOGGLE_INTERVAL)

    def send_command(self, command, expect_response, pre_response, post_response):
        response = b""
        self._serial.write(command)
        if expect_response:
            t = 0
            while t < self._rx_time_out:
                if self._serial.in_waiting > 0:
                    t = 0
                    response += self._serial.read(self._serial.in_waiting)
                if response.startswith(pre_response) and response.endswith(post_response):
                    break
                time.sleep(0.1)
                t += 0.1
            else:
                self.raise_timeout_exception()
        return response

    def close(self):
        self._serial.close()

    @classmethod
    def get_settings_controls(cls):
        return {
            "serial_port": {
                "label": "Serial port",
                "control": wx.ComboBox,
                "data": get_available_serial_ports,
                "default": ""
            },
            "baud_rate": {
                "label": "Baud rate",
                "control": wx.ComboBox,
                "data": list(map(str, cls._BAUD_RATES)),
                "default": str(cls._DEFAULT_BAUD_RATE)
            },
            "parity": {
                "label": "Parity",
                "control": wx.ComboBox,
                "data": list(cls._PARITY_VALUES.keys()),
                "default": cls._DEFAULT_PARITY
            },
            "stop_bits": {
                "label": "Stop bits",
                "control": wx.ComboBox,
                "data": list(map(str, cls._STOP_BITS)),
                "default": str(cls._DEFAULT_STOP_BITS)
            },
            "data_bits": {
                "label": "Data bits",
                "control": wx.ComboBox,
                "data": list(map(str, cls._DATA_BITS)),
                "default": str(cls._DEFAULT_DATA_BITS)
            }
        }


if __name__ == "__main__":

    import pylint
    from tests.unit_tests.test_serial_port_interface import TestSerialPortInterface

    TestSerialPortInterface().run(True)
    pylint.run_pylint([__file__])
