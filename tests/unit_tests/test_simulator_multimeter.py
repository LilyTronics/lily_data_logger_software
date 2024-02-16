"""
Test the model for the multimeter simulator
"""

from src.models.instruments.simulator_multimeter import simulator_multimeter
from src.models.interfaces import Interfaces
from src.simulators import Simulators
from tests.unit_tests.lib.test_suite import TestSuite


class TestSimulatorMultimeter(TestSuite):

    _interface = None

    def setup(self):
        Simulators.start_simulators(self.log)
        self.log.debug("Get interface")
        interface_class = Interfaces.get_interface_by_name(
            simulator_multimeter.get_interface_type())
        self.fail_if(interface_class is None,
                     f"No interface found for: {simulator_multimeter.get_interface_type()}")
        self.log.debug("Initialize interface")
        settings = simulator_multimeter.get_interface_settings()
        self._interface = interface_class(**settings)
        simulator_multimeter.set_interface_object(self._interface)
        simulator_multimeter.initialize()

    def test_properties(self):
        self.fail_if(simulator_multimeter.get_name() != "Simulator multimeter",
                     f"The name is not correct '{simulator_multimeter.get_name()}'")
        self.fail_if(simulator_multimeter.get_info() == simulator_multimeter.DEFAULT_INFO,
                     "The info has the default value")

    def test_dc_voltage(self):
        self.log.debug("Test DC voltage")
        value = simulator_multimeter.get_value("Get DC voltage")
        self.log.debug(f"Value: {value}")
        self.fail_if(not isinstance(value, float), f"Float expected, but got {type(value)}")

    def test_dc_current(self):
        self.log.debug("Test DC current")
        value = simulator_multimeter.get_value("Get DC current")
        self.log.debug(f"Value: {value}")
        self.fail_if(not isinstance(value, float), f"Float expected, but got {type(value)}")

    def teardown(self):
        Simulators.stop_simulators(self.log)
        if self._interface is not None:
            self._interface.close()


if __name__ == "__main__":

    import pylint

    TestSimulatorMultimeter().run()
    pylint.run_pylint([__file__])
