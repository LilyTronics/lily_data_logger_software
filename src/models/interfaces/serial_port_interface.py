"""
Serial port interface.
"""

import serial
import time

from src.models.interfaces.interface import Interface


class SerialPortInterface(Interface):

    NAME = "Serial port"
    DEFAULT_TERMINATOR = b"\n"
    DEFAULT_TIMEOUT = 5
    DEFAULT_BAUD_RATE = 9600

    _TOGGLE_INTERVAL = 0.005

    def __init__(self, port_name, baud_rate=DEFAULT_BAUD_RATE, rx_timeout=DEFAULT_TIMEOUT,
                 terminator=DEFAULT_TERMINATOR, tx_timeout=0):
        if tx_timeout == 0:
            tx_timeout = rx_timeout
        self._rx_time_out = rx_timeout
        self._terminator = terminator
        self._serial = serial.Serial(port_name, baudrate=int(baud_rate), write_timeout=tx_timeout)

    def toggle_dtr(self):
        for value in (True, False, True):
            self._serial.dtr = value
            time.sleep(self._TOGGLE_INTERVAL)

    def send_command(self, command, expect_response=True):
        response = b""
        self._serial.write(command + self._terminator)
        if expect_response:
            t = 0
            while t < self._rx_time_out:
                if self._serial.in_waiting > 0:
                    t = 0
                    response += self._serial.read(self._serial.in_waiting)
                if response.endswith(self._terminator):
                    break
                time.sleep(0.1)
                t += 0.1
            else:
                self.raise_timeout_exception()
        return response

    def close(self):
        self._serial.close()


if __name__ == "__main__":

    from tests.unit_tests.test_serial_port_interface import TestSerialPortInterface

    TestSerialPortInterface().run()
