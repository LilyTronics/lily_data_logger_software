"""
Running simulators.
"""

from src.simulators.multimeter_udp import MultimeterUdp


SIMULATORS = []


def start_simulators():
    for simulator in [MultimeterUdp]:
        _start_simulator(simulator)


def stop_simulators():
    for simulator in SIMULATORS:
        simulator.stop()


def _start_simulator(simulator_class):
    matches = list(filter(lambda x: x.__class__ == simulator_class, SIMULATORS))
    if len(matches) == 0:
        try:
            sim_object = simulator_class()
            SIMULATORS.append(sim_object)
        except Exception as e:
            raise Exception("Could not initialize '{}': {}".format(simulator_class.__name__, e))
    else:
        sim_object = matches[0]
    try:
        sim_object.start()
    except Exception as e:
        raise Exception("Could not start '{}': {}".format(simulator_class.__name__, e))


if __name__ == "__main__":

    from tests.unit_tests.test_simulators import TestStartStopSimulators

    TestStartStopSimulators().run()
