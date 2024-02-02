"""
Test for the configuration model.
"""

import os

from src.models.configuration import Configuration
from tests.test_suite import TestSuite


class TestConfiguration(TestSuite):

    def setup(self):
        self._filename = "test_config.json"

    def _check_default_values(self, config):
        self.fail_if(config.get_sample_time() != 3, "The default sample time is incorrect")
        self.fail_if(config.get_end_time() != 60, "The default end time is incorrect")
        self.fail_if(config.get_continuous_mode(), "The default continuous mode is incorrect")
        self.fail_if(config.get_instruments() != [], "The default instruments list is incorrect")
        self.fail_if(config.get_measurements() != [], "The default measurements list is incorrect")
        self.fail_if(config.get_process_steps() != [], "The default process steps list is incorrect")
        self.fail_if(config.get_filename() != "<new configuration>", "The default filename is incorrect")
        self.fail_if(config.is_changed(), "The changed flag is incorrect")

    def test_empty_configuration(self):
        conf = Configuration()
        self._check_default_values(conf)

    def test_general_settings(self):
        conf = Configuration()

        current_value = conf.get_sample_time()
        new_value = current_value + 2
        conf.set_sample_time(new_value)
        self.fail_if(conf.get_sample_time() != new_value, "Failed to store the sample time")
        self.fail_if(not conf.is_changed(), "The changed flag is incorrect")

        conf._is_changed = False
        current_value = conf.get_end_time()
        new_value = current_value + 2
        conf.set_end_time(new_value)
        self.fail_if(conf.get_end_time() != new_value, "Failed to store the end time")
        self.fail_if(not conf.is_changed(), "The changed flag is incorrect")

        conf._is_changed = False
        current_value = conf.get_continuous_mode()
        new_value = not current_value
        conf.set_continuous_mode(new_value)
        self.fail_if(conf.get_continuous_mode() != new_value, "Failed to store the continuous mode")
        self.fail_if(not conf.is_changed(), "The changed flag is incorrect")

    def test_save_to_load_from_file(self):
        conf = Configuration()
        conf.set_sample_time(10)
        conf.set_end_time(180)
        conf.set_continuous_mode(True)
        conf.save_to_file(self._filename)
        self.fail_if(conf.get_filename() != self._filename, "The filename is incorrect")

        conf = Configuration()
        conf.load_from_file(self._filename)
        self.fail_if(conf.get_sample_time() != 10, "The sample time is incorrect")
        self.fail_if(conf.get_end_time() != 180, "The end time is incorrect")
        self.fail_if(not conf.get_continuous_mode(), "The continuous mode is incorrect")
        self.fail_if(conf.get_filename() != self._filename, "The filename is incorrect")
        self.fail_if(conf.is_changed(), "The changed flag is incorrect")

    def test_load_empty_file(self):
        open(self._filename, "w").close()
        conf = Configuration()
        try:
            conf.load_from_file(self._filename)
            self.fail("Reading empty file passed, expected an exception")
        except Exception as e:
            self.log.debug("Error message:\n{}".format(e))
            self.fail_if("Error reading file: {}".format(self._filename) not in str(e), "Error message is incorrect")
        self._check_default_values(conf)

    def test_load_invalid_file(self):
        conf = Configuration()
        with open(self._filename, "w") as fp:
            fp.write("invalid file format\n")
        try:
            conf.load_from_file(self._filename)
            self.fail("Reading empty file passed, expected an exception")
        except Exception as e:
            self.log.debug("Error message:\n{}".format(e))
            self.fail_if("Error reading file: {}".format(self._filename) not in str(e), "Error message is incorrect")
        self._check_default_values(conf)

    def teardown(self):
        if os.path.isfile(self._filename):
            os.remove(self._filename)


if __name__ == "__main__":

    TestConfiguration().run(True)
