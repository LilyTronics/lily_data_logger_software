"""
Running simulators.
"""

from src.simulators.multimeter_udp import MultimeterUdp


SIMULATORS = []


def start_simulators(logger):
    logger.debug("Starting simulators")
    for simulator in [MultimeterUdp]:
        _start_simulator(simulator, logger)
    _log_running_simulators(logger)


def stop_simulators(logger):
    logger.debug("Stopping simulators")
    for simulator in SIMULATORS:
        name = simulator.__class__.__name__
        logger.debug("Stop simulator '{}'".format(name))
        try:
            simulator.stop()
        except Exception as e:
            logger.error("Could not stop simulator '{}': {}".format(name, e))
    _log_running_simulators(logger)


def _log_running_simulators(logger):
    running = list(filter(lambda x: x.is_running(), SIMULATORS))
    if len(running) > 0:
        logger.debug("Running simulators: {}".format(
            ", ".join(map(lambda x: "'{}'".format(x.__class__.__name__), running))))
    else:
        logger.debug("No simulators running")


def _start_simulator(simulator_class, logger):
    name = simulator_class.__name__
    matches = list(filter(lambda x: x.__class__ == simulator_class, SIMULATORS))
    sim_object = None
    if len(matches) == 0:
        try:
            logger.debug("Initialize simulator '{}'".format(name))
            sim_object = simulator_class()
            SIMULATORS.append(sim_object)
        except Exception as e:
            logger.error("Could not initialize simulator '{}': {}".format(name, e))
    else:
        sim_object = matches[0]
    if sim_object is not None:
        try:
            logger.debug("Start simulator '{}'".format(name))
            sim_object.start()
        except Exception as e:
            logger.error("Could not start simulator '{}': {}".format(name, e))


if __name__ == "__main__":

    from tests.unit_tests.test_start_stop_simulators import TestStartStopSimulators

    TestStartStopSimulators().run()
