"""
Test the model for the Arduino DAQ.
For testing, loopback connectors should be installed on the Arduino.
"""

from src.models.instruments.arduino_daq import arduino_daq
from src.models.interfaces import get_interface_by_name
from src.models.list_serial_ports import get_available_serial_ports
from tests.test_environment.check_arduino_daq import get_arduino_daq_serial_port
from tests.unit_tests.lib.test_suite import TestSuite


class TestArduinoDAQ(TestSuite):

    def _set_interface(self, port_name):
        self.log.debug("Get interface")
        interface_class = get_interface_by_name(arduino_daq.get_interface_type())
        self.fail_if(interface_class is None, "No interface found for: {}".format(arduino_daq.get_interface_type()))
        self.log.debug("Initialize interface")
        settings = arduino_daq.get_interface_settings()
        self._interface = interface_class(**settings)
        arduino_daq.set_interface_object(self._interface)
        arduino_daq.initialize()

    def setup(self):
        ports = get_available_serial_ports()
        self.fail_if(len(ports) == 0, "No serial ports found")
        port_name = get_arduino_daq_serial_port(ports)
        self.fail_if(port_name is None, "No power supply found")
        self._set_interface(port_name)

    def test_properties(self):
        self.log.debug("Check name")
        self.fail_if(arduino_daq.get_name() != "Arduino Uno DAQ",
                     "The name is not correct {}".format(arduino_daq.get_name()))
        self.log.debug("Check info")
        self.fail_if(arduino_daq.get_info() == arduino_daq.DEFAULT_INFO,
                     "The info has the default value")

    def test_digital_io(self):
        def _test_io(d_out, d_in):
            self.log.debug("Test D{} to D{}".format(d_out, d_in))
            for state in (1, 0):
                arduino_daq.set_value("D{} set state".format(d_out), state)
                value = arduino_daq.get_value("D{} get state".format(d_in))
                self.log.debug("Set output: {}, read input: {}".format(state, value))
                self.fail_if(state != value, "IO did not change to the correct value")
            # Make output input by reading
            arduino_daq.get_value("D{} get state".format(d_out))

        for d in range(2, 13, 2):
            _test_io(d, d + 1)
            _test_io(d + 1, d)

    def test_analog_inputs(self):
        expected = 5
        for a in range(6):
            expected -= (5 / 7)
            self.log.debug("Read voltage A{}".format(a))
            value = arduino_daq.get_value("A{} get voltage".format(a))
            self.log.debug("Voltage : {} V".format(value))
            self.log.debug("Expected: {:.3f} V".format(expected))
            self.fail_if(abs(value - expected) > 0.01,
                         "Voltage difference is too big {:.3f} V".format(abs(value - expected)))

    def teardown(self):
        self._interface.close()


if __name__ == "__main__":

    TestArduinoDAQ().run()
