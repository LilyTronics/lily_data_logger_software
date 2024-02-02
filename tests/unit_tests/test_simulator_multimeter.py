"""
Test the model for the multimeter simulator
"""

from src.models.instruments.simulator_multimeter import simulator_multimeter
from tests.unit_tests.lib.test_suite import TestSuite


class TestSimulatorMultimeter(TestSuite):

    def test_properties(self):
        self.fail_if(simulator_multimeter.get_name() != "Simulator multimeter",
                     "The name is not correct '{}'".format(simulator_multimeter.get_name()))
        self.fail_if(simulator_multimeter.get_info() == simulator_multimeter.DEFAULT_INFO,
                     "The info has the default value")


if __name__ == "__main__":

    TestSimulatorMultimeter().run()
