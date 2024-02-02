"""
Model for the multimeter simulator
"""

from src.models.instrument import Instrument


simulator_multimeter = Instrument({
    "name": "Simulator multimeter",
    "info": "Read random values for voltage (4.9...5.1V) and current (0.39...0.41)"
})


if __name__ == "__main__":

    from tests.unit_tests.test_simulator_multimeter import TestSimulatorMultimeter

    TestSimulatorMultimeter().run()
