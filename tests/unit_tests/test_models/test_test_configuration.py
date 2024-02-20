"""
Test for the test configuration.
"""

from tests.test_environment.test_configuration import TestConfiguration
from tests.unit_tests.lib.test_suite import TestSuite


class TestTestConfiguration(TestSuite):

    def test_default(self):
        conf = TestConfiguration()
        self.fail_if(conf.get_sample_time() != 2, "The sample time is not 2")
        self.fail_if(conf.get_end_time() != 7, "The end time is not 7")
        self.fail_if(len(conf.get_instruments()) > 0, "One or more instruments are present")
        self.fail_if(len(conf.get_measurements()) > 0, "One or more measurements are present")

    def test_add_instrument(self):
        conf = TestConfiguration(True)
        self.fail_if(len(conf.get_instruments()) == 0, "No instrument was added")

    def test_add_measurement(self):
        conf = TestConfiguration(True, True)
        self.fail_if(len(conf.get_instruments()) == 0, "No instrument was added")
        self.fail_if(len(conf.get_measurements()) == 0, "No measurement was added")

    def test_add_measurement_no_instrument(self):
        conf = TestConfiguration(False, True)
        self.fail_if(len(conf.get_instruments()) > 0, "One or more instruments are present")
        self.fail_if(len(conf.get_measurements()) > 0, "One or more measurements are present")


if __name__ == "__main__":

    import pylint

    TestTestConfiguration().run(True)
    pylint.run_pylint([__file__])
