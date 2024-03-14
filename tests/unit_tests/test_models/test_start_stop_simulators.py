"""
Test the simulators package.
"""

from src.simulators import Simulators
from tests.unit_tests.lib.test_suite import TestSuite


class TestStartStopSimulators(TestSuite):

    def _check_running_simulators(self, expected_running):
        for simulator in Simulators.get_running_simulators():
            self.log.debug(f"'{simulator.__class__.__name__}' running: {simulator.is_running()}")
            self.fail_if(simulator.is_running() is not expected_running,
                         f"Simulator '{simulator.__class__.__name__}' is not running")

    def test_start_simulators(self):
        self.log.debug("Start simulators")
        try:
            Simulators.start_simulators(self.log)
        except Exception as e:
            self.log.error(e)
            self.fail("Could not start the simulators")
        self._check_running_simulators(True)

        self.log.debug("Start simulators while already running")
        try:
            Simulators.start_simulators(self.log)
        except Exception as e:
            self.log.error(e)
            self.fail("An error occurred when starting the simulators while already running")
        self._check_running_simulators(True)

    def test_stop_start_single_simulator(self):
        self.log.debug("Stop a simulator")
        running_simulators = Simulators.get_running_simulators()
        running_simulators[0].stop()
        self.fail_if(running_simulators[0].is_running(),
                     "Simulator is still running after stop command")
        self.log.debug("Start simulators")
        Simulators.start_simulators(self.log)
        self._check_running_simulators(True)

    def test_stop_start_all_simulators(self):
        self.log.debug("Stop simulators")
        Simulators.stop_simulators(self.log)
        self._check_running_simulators(False)
        self.log.debug("Start simulators")
        Simulators.start_simulators(self.log)
        self._check_running_simulators(True)

    def test_stop_simulators(self):
        self.log.debug("Stop simulators")
        Simulators.stop_simulators(self.log)
        self._check_running_simulators(False)
        self.log.debug("Stop simulators again")
        Simulators.stop_simulators(self.log)
        self._check_running_simulators(False)


if __name__ == "__main__":

    TestStartStopSimulators().run()
