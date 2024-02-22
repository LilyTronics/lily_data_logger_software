"""
Test the model for the multimeter simulator
"""

from src.models.instruments.simulator_multimeter import simulator_multimeter
from src.models.interfaces import Interfaces
from src.simulators import Simulators
from tests.unit_tests.lib.test_suite import TestSuite


class TestSimulatorMultimeter(TestSuite):

    _N_SAMPLES = 10
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
        voltages = []
        self.log.debug(f"Get {self._N_SAMPLES} voltages")
        for _ in range(self._N_SAMPLES):
            response = simulator_multimeter.process_channel("Get DC voltage")
            self.fail_if(not isinstance(response, float), "response should be float")
            voltages.append(response)
        self.log.debug(f"Voltages: {voltages}")
        self.fail_if(min(voltages) < 4.9, f"Voltage < 4.9 found: {min(voltages)}")
        self.fail_if(max(voltages) > 5.1, f"Voltage > 5.1 found: {max(voltages)}")

    def test_dc_current(self):
        currents = []
        self.log.debug(f"Get {self._N_SAMPLES} currents")
        for _ in range(self._N_SAMPLES):
            response = simulator_multimeter.process_channel("Get DC current")
            self.fail_if(not isinstance(response, float), "response should be float")
            currents.append(response)
        self.log.debug(f"Currents: {currents}")
        self.fail_if(min(currents) < 0.39, f"Current < 0.39 found: {min(currents)}")
        self.fail_if(max(currents) > 0.41, f"Current > 0.41 found: {max(currents)}")

    def teardown(self):
        Simulators.stop_simulators(self.log)
        if self._interface is not None:
            self._interface.close()


if __name__ == "__main__":

    import pylint

    TestSimulatorMultimeter().run(True)
    pylint.run_pylint([__file__])
