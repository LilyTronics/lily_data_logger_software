"""
Test the simulators package.
"""

from src.simulators import SIMULATORS
from src.simulators import start_simulators
from src.simulators import stop_simulators
from tests.test_suite import TestSuite


class TestStartStopSimulators(TestSuite):

    def _check_running_simulators(self, expected_running):
        for simulator in SIMULATORS:
            self.log.debug("'{}' running: {}".format(simulator.__class__.__name__, simulator.is_running()))
            self.fail_if(simulator.is_running() is not expected_running,
                         "Simulator '{}' is not running".format(simulator.__class__.__name__))

    def test_start_simulators(self):
        self.log.debug("Start simulators")
        try:
            start_simulators()
        except Exception as e:
            self.log.error(e)
            self.fail("Could not start the simulators")
        self._check_running_simulators(True)

        self.log.debug("Start simulators while already running")
        try:
            start_simulators()
        except Exception as e:
            self.log.error(e)
            self.fail("An error occurred when starting the simulators while already running")
        self._check_running_simulators(True)

    def test_stop_start_single_simulator(self):
        self.log.debug("Stop a simulator")
        SIMULATORS[0].stop()
        self.fail_if(SIMULATORS[0].is_running(), "Simulator is still running after stop command")
        self.log.debug("Start simulators")
        start_simulators()
        self._check_running_simulators(True)

    def test_stop_start_all_simulators(self):
        self.log.debug("Stop simulators")
        stop_simulators()
        self._check_running_simulators(False)
        self.log.debug("Start simulators")
        start_simulators()
        self._check_running_simulators(True)

    def test_stop_simulators(self):
        self.log.debug("Stop simulators")
        stop_simulators()
        self._check_running_simulators(False)
        self.log.debug("Stop simulators again")
        stop_simulators()
        self._check_running_simulators(False)

    @staticmethod
    def teardown():
        del SIMULATORS[:]


if __name__ == "__main__":

    TestStartStopSimulators().run()
