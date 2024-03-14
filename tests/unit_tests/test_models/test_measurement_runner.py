"""
Test for the measurement runner.
"""

from src.models.measurement_runner import MeasurementRunner
from src.simulators import Simulators
from tests.unit_tests.lib.test_suite import TestSuite
from tests.test_environment.test_configurations import TestConfigurations


class TestMeasurementRunner(TestSuite):

    _runner = None
    _messages = []

    def _callback(self, *args):
        self._messages.append(args)
        self.log.debug(f"Callback message: ({args})")

    def setup(self):
        Simulators.start_simulators(self.log)
        conf = TestConfigurations.get_unit_test_configuration()
        self._runner = MeasurementRunner(conf, self._callback)

    def test_start_stop(self):
        del self._messages[:]
        self.log.debug("Start measurement runner")
        self._runner.start()
        self.fail_if(not self._runner.is_running(), "Measurement runner is not running")
        self.log.debug("Wait a few seconds")
        self.sleep(3.1)
        self.log.debug("Stop measurement runner")
        self._runner.stop()
        self.fail_if(self._runner.is_running(), "Measurement runner is not stopped")
        self.fail_if(len(self._messages) < 3, "Not enough messages received")
        self.log.debug(f"Elapsed time: {self._runner.get_elapsed_time():.1f} seconds")
        self.fail_if(self._runner.get_elapsed_time() < 3, "Elapsed time is too small")
        self.fail_if(self._runner.get_elapsed_time() > 4, "Elapsed time is too big")

    def test_start_until_finished(self):
        del self._messages[:]
        self.log.debug("Start measurement runner")
        self._runner.start()
        self.log.debug("Wait for measurement runner to finish")
        self.fail_if(not self._runner.is_running(), "Measurement runner is not running")
        if not self.wait_for(self._runner.is_running, False, 10, 0.1):
            self.fail("Measurement runner did not finish by itself")
        self.fail_if(self._runner.is_running(), "Measurement runner is not stopped")
        self.fail_if(len(self._messages) < 6, "Not enough messages received")
        self.log.debug(f"Elapsed time: {self._runner.get_elapsed_time():.1f} seconds")
        self.fail_if(self._runner.get_elapsed_time() < 7, "Elapsed time is too small")
        self.fail_if(self._runner.get_elapsed_time() > 7.2, "Elapsed time is too small")

    def teardown(self):
        Simulators.stop_simulators(self.log)


if __name__ == "__main__":

    TestMeasurementRunner().run()
