"""
Serial port interface.
The unit test requires a serial port, with a loopback connector connected (automatically detected).
"""

from src.models.list_serial_ports import get_available_serial_ports
from src.models.interfaces.serial_port_interface import SerialPortInterface
from tests.test_environment.check_serial_loopback import get_serial_loopback_port
from tests.unit_tests.lib.test_suite import TestSuite


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
        self.fail_if(response != b"", "Invalid response received: {}".format(response))

    def teardown(self):
        if self._serial is not None:
            self._serial.close()


if __name__ == "__main__":

    TestSerialPortInterface().run()
