"""
Test the model for the temperature meter simulator
"""

from src.models.instruments.simulator_temperature_meter import simulator_temperature_meter
from src.models.interfaces import Interfaces
from src.simulators import Simulators
from tests.unit_tests.lib.test_suite import TestSuite


class TestSimulatorTemperatureMeter(TestSuite):

    _N_SAMPLES = 10
    _interface = None

    def setup(self):
        Simulators.start_simulators(self.log)
        self.log.debug("Get interface")
        interface_class = Interfaces.get_interface_by_name(
            simulator_temperature_meter.get_interface_type())
        self.fail_if(interface_class is None,
                     f"No interface found for: {simulator_temperature_meter.get_interface_type()}")
        self.log.debug("Initialize interface")
        settings = simulator_temperature_meter.get_interface_settings()
        self._interface = interface_class(**settings)
        simulator_temperature_meter.set_interface_object(self._interface)
        simulator_temperature_meter.initialize()

    def test_properties(self):
        self.fail_if(simulator_temperature_meter.get_name() != "Simulator temperature meter",
                     f"The name is not correct '{simulator_temperature_meter.get_name()}'")
        self.fail_if(simulator_temperature_meter.get_info() ==
                     simulator_temperature_meter.DEFAULT_INFO,
                     "The info has the default value")

    def test_dc_voltage(self):
        temperatures = []
        self.log.debug(f"Get {self._N_SAMPLES} temperatures")
        for _ in range(self._N_SAMPLES):
            response = simulator_temperature_meter.get_value("Get temperature")
            self.fail_if(not isinstance(response, float), "response should be float")
            temperatures.append(response)
        self.log.debug(f"Temperatures: {temperatures}")
        self.fail_if(min(temperatures) < 15, f"Temperature < 15 found: {min(temperatures)}")
        self.fail_if(max(temperatures) > 25, f"Temperature > 25 found: {max(temperatures)}")

    def teardown(self):
        Simulators.stop_simulators(self.log)
        if self._interface is not None:
            self._interface.close()


if __name__ == "__main__":

    import pylint

    TestSimulatorTemperatureMeter().run()
    pylint.run_pylint([__file__])
