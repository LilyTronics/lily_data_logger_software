"""
Running simulators.
"""

from src.simulators.multimeter_udp import MultimeterUdp
from src.simulators.temperature_chamber_tcp import TemperatureChamberTcp
from unit_test.test_suite import TestSuite


_SIMULATORS = []


def start_simulators():
    for simulator in [MultimeterUdp, TemperatureChamberTcp]:
        _start_simulator(simulator)


def stop_simulators():
    for simulator in _SIMULATORS:
        simulator.stop()


def _start_simulator(simulator_class):
    matches = list(filter(lambda x: x.__class__ == simulator_class, _SIMULATORS))
    if len(matches) == 0:
        try:
            sim_object = simulator_class()
            _SIMULATORS.append(sim_object)
        except Exception as e:
            raise Exception('Could not initialize {}: {}'.format(simulator_class.__name__, e))
    else:
        sim_object = matches[0]
    try:
        sim_object.start()
    except Exception as e:
        raise Exception('Could not start {}: {}'.format(simulator_class.__name__, e))


class TestStartStopSimulators(TestSuite):

    def _check_running_simulators(self, expected_running):
        for simulator in _SIMULATORS:
            self.log.debug('{} running: {}'.format(simulator.__class__.__name__, simulator.is_running()))
            self.fail_if(simulator.is_running() is not expected_running,
                         'Simulator {} is not running'.format(simulator.__class__.__name__))

    def test_start_simulators(self):
        self.log.debug('Start simulators')
        try:
            start_simulators()
        except Exception as e:
            self.log.error(e)
            self.fail('Could not start the simulators')
        self._check_running_simulators(True)

        self.log.debug('Start simulators while already running')
        try:
            start_simulators()
        except Exception as e:
            self.log.error(e)
            self.fail('An error occurred when starting the simulators while already running')
        self._check_running_simulators(True)

    def test_stop_start_single_simulator(self):
        self.log.debug('Stop a simulator')
        _SIMULATORS[0].stop()
        self.fail_if(_SIMULATORS[0].is_running(), 'Simulator is still running after stop command')
        self.log.debug('Start simulators')
        start_simulators()
        self._check_running_simulators(True)

    def test_stop_start_all_simulators(self):
        self.log.debug('Stop simulators')
        stop_simulators()
        self._check_running_simulators(False)
        self.log.debug('Start simulators')
        start_simulators()
        self._check_running_simulators(True)

    def test_stop_simulators(self):
        self.log.debug('Stop simulators')
        stop_simulators()
        self._check_running_simulators(False)
        self.log.debug('Stop simulators again')
        stop_simulators()
        self._check_running_simulators(False)

    @staticmethod
    def teardown():
        del _SIMULATORS[:]


if __name__ == '__main__':

    TestStartStopSimulators().run()
