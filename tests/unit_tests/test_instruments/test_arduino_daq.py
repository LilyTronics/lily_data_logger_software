"""
Test the model for the Arduino DAQ.
For testing, loopback connectors should be installed on the Arduino.
"""

from src.models.instruments.arduino_daq import arduino_daq
from src.models.interfaces import Interfaces
from src.models.list_serial_ports import get_available_serial_ports
from tests.test_environment.check_arduino_daq import get_arduino_daq_serial_port
from tests.unit_tests.lib.test_suite import TestSuite


class TestArduinoDAQ(TestSuite):

    _interface = None

    def _set_interface(self, port_name):
        self.log.debug("Get interface")
        interface_class = Interfaces.get_interface_by_name(arduino_daq.get_interface_type())
        self.fail_if(interface_class is None,
                     f"No interface found for: {arduino_daq.get_interface_type()}")
        self.log.debug("Initialize interface")
        settings = arduino_daq.get_interface_settings()
        settings["serial_port"] = port_name
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
        self.fail_if(arduino_daq.get_name() != "Arduino DAQ",
                     f"The name is not correct {arduino_daq.get_name()}")
        self.log.debug("Check info")
        self.fail_if(arduino_daq.get_info() == arduino_daq.DEFAULT_INFO,
                     "The info has the default value")

    def test_digital_io(self):
        def _test_io(d_out, d_in):
            self.log.debug(f"Test D{d_out} to D{d_in}")
            for state in (1, 0):
                arduino_daq.process_channel(f"D{d_out} set state", state)
                value = arduino_daq.process_channel(f"D{d_in} get state")
                self.log.debug(f"Set output: {state}, read input: {value}")
                self.fail_if(state != value, "IO did not change to the correct value")
            # Make output input by reading
            arduino_daq.process_channel(f"D{d_out} get state")

        for d in range(2, 13, 2):
            _test_io(d, d + 1)
            _test_io(d + 1, d)

    def test_analog_inputs(self):
        expected = 5
        for ch in range(6):
            expected -= (5 / 7)
            self.log.debug(f"Read voltage A{ch}")
            value = arduino_daq.process_channel(f"A{ch} get voltage")
            self.log.debug(f"Voltage : {value} V")
            self.log.debug(f"Expected: {expected:.3f} V")
            diff = abs(value - expected)
            self.fail_if(diff > 0.01,
                         f"Voltage difference is too big {diff:.3f} V")

    def teardown(self):
        if self._interface is not None:
            self._interface.close()


if __name__ == "__main__":

    import pylint

    TestArduinoDAQ().run()
    pylint.run_pylint([__file__])
