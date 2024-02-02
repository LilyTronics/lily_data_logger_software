"""
Serial port interface.
The unit test requires a serial port, with a loopback connector connected (automatically detected).
"""

import serial
import time

from src.models.list_serial_ports import get_available_serial_ports
from src.models.interfaces.interface import Interface
from tests.test_environment.check_serial_loopback import get_serial_loopback_port
from tests.test_suite import TestSuite


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


class TestSerialPortInterface(TestSuite):

    _CHECK_FOR_LOOPBACK_DATA = b"check_for_loopback"
    _TEST_COMMAND = b"serial_port_test"
    _RX_TIMEOUT = 1

    _serial = None

    def setup(self):
        self.log.info("Get available serial ports")
        ports = get_available_serial_ports()
        self.fail_if(len(ports) == 0, "No serial ports available")
        port = get_serial_loopback_port(ports)
        self.log.info("Loopback found on port: {}".format(port))
        self._serial = SerialPortInterface(port, self._RX_TIMEOUT)

    def test_send_command(self):
        response = self._serial.send_command(self._TEST_COMMAND)
        self.fail_if(self._TEST_COMMAND + b"\n" != response, "Invalid response received: {}".format(response))

    def test_no_response(self):
        response = self._serial.send_command(self._TEST_COMMAND, False)
        self.fail_if(response is not None, "Invalid response received: {}".format(response))

    def teardown(self):
        if self._serial is not None:
            self._serial.close()


if __name__ == "__main__":

    TestSerialPortInterface().run()
