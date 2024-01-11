"""
Serial port interface.
The unit test requires a serial port, with a loopback connector connected (automatically detected).
"""

import lily_unit_test
import serial
import time

from src.models.list_serial_ports import get_available_serial_ports
from src.models.interfaces.interface import Interface


class SerialPortInterface(Interface):

    DEFAULT_TERMINATOR = b'\n'
    DEFAULT_TIMEOUT = 5

    def __init__(self, port_name, rx_timeout=DEFAULT_TIMEOUT, terminator=DEFAULT_TERMINATOR, tx_timeout=0):
        if tx_timeout == 0:
            tx_timeout = rx_timeout
        self._rx_time_out = rx_timeout
        self._terminator = terminator
        self._serial = serial.Serial(port_name, write_timeout=tx_timeout)

    def send_command(self, command):
        response = b''
        self._serial.write(command + self._terminator)
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


class TestSerialPortInterface(lily_unit_test.TestSuite):

    _CHECK_FOR_LOOPBACK_DATA = b'check_for_loopback'
    _TEST_COMMAND = b'serial_port_test'
    _RX_TIMEOUT = 1

    _serial = None

    def _check_for_loopback(self, port_name):
        self.log.debug('Check for loopback on port: {}'.format(port_name))
        with serial.Serial(port_name, write_timeout=0.2) as s:
            s.write(self._CHECK_FOR_LOOPBACK_DATA)
            i = 5
            rx_data = b''
            while i > 0:
                if s.in_waiting > 0:
                    rx_data += s.read(s.in_waiting)
                if rx_data == self._CHECK_FOR_LOOPBACK_DATA:
                    break
                time.sleep(0.1)
                i -= 1
            else:
                raise Exception('Loopback data not found (timeout)')

    def setup(self):
        self.log.info('Get available serial ports')
        ports = get_available_serial_ports()
        self.fail_if('no ports' in ports, 'No serial ports available')
        port = None
        for port in ports:
            try:
                self._check_for_loopback(port)
                break
            except Exception as e:
                self.log.debug(e)
        else:
            self.fail('No port with loopback found')
        self.log.info('Loopback found on port: {}'.format(port))
        self._serial = SerialPortInterface(port, self._RX_TIMEOUT)

    def test_send_command(self):
        response = self._serial.send_command(self._TEST_COMMAND)
        self.fail_if(self._TEST_COMMAND + b'\n' != response, 'Invalid response received: {}'.format(response))

    def teardown(self):
        if self._serial is not None:
            self._serial.close()


if __name__ == '__main__':

    TestSerialPortInterface().run()
