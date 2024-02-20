"""
Running simulators.
"""

from src.simulators.multimeter_udp import MultimeterUdp
from src.simulators.temperature_meter_tcp import TemperatureMeterTcp


class Simulators:

    _SIMULATOR_CLASSES = [
        MultimeterUdp,
        TemperatureMeterTcp
    ]

    _SIMULATORS = []

    def __init__(self):
        raise RuntimeError("No instance of this class is permitted")

    #########
    # Pubic #
    #########

    @classmethod
    def get_running_simulators(cls):
        return list(filter(lambda x: x.is_running(), cls._SIMULATORS))

    @classmethod
    def start_simulators(cls, logger):
        logger.debug("Starting simulators")
        for simulator in cls._SIMULATOR_CLASSES:
            cls._start_simulator(simulator, logger)
        cls._log_running_simulators(logger)

    @classmethod
    def stop_simulators(cls, logger):
        logger.debug("Stopping simulators")
        for simulator in cls._SIMULATORS:
            name = simulator.__class__.__name__
            logger.debug(f"Stop simulator '{name}'")
            try:
                simulator.stop()
            except Exception as e:
                logger.error(f"Could not stop simulator '{name}': {e}")
        cls._log_running_simulators(logger)

    ###########
    # Private #
    ###########

    @classmethod
    def _log_running_simulators(cls, logger):
        running = cls.get_running_simulators()
        if len(running) > 0:
            running_sims = ", ".join(map(lambda x: f"'{x.__class__.__name__}'", running))
            logger.debug(f"Running simulators: {running_sims}")
        else:
            logger.debug("No simulators running")

    @classmethod
    def _start_simulator(cls, simulator_class, logger):
        name = simulator_class.__name__
        matches = list(filter(lambda x: x.__class__ == simulator_class, cls._SIMULATORS))
        sim_object = None
        if len(matches) == 0:
            try:
                logger.debug(f"Initialize simulator '{name}'")
                sim_object = simulator_class()
                cls._SIMULATORS.append(sim_object)
            except Exception as e:
                logger.error(f"Could not initialize simulator '{name}': {e}")
        else:
            sim_object = matches[0]
        if sim_object is not None:
            try:
                logger.debug(f"Start simulator '{name}'")
                sim_object.start()
            except Exception as e:
                logger.error(f"Could not start simulator '{name}': {e}")


if __name__ == "__main__":

    import pylint
    from tests.unit_tests.test_models.test_start_stop_simulators import TestStartStopSimulators

    TestStartStopSimulators().run()
    pylint.run_pylint([__file__])
