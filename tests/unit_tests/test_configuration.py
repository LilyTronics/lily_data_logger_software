"""
Test for the configuration model.
"""

import os

from src.models.configuration import Configuration
from tests.unit_tests.lib.test_suite import TestSuite


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

    def test_add_update_instrument(self):
        conf = Configuration()
        name = "Test instrument"
        settings = {
            conf.KEY_INSTRUMENT_NAME: "Simulator multimeter",
            conf.KEY_INSTRUMENT_SETTINGS: {
                "ip_address": "localhost",
                "ip_port": 17000,
                "rx_timeout": 0.2
            }
        }
        self.log.debug("Add instrument")
        conf.update_instrument(name, name, settings)
        self.fail_if(len(conf.get_instruments()) != 1, "Instrument was not added")
        instrument = conf.get_instrument(name)
        self.fail_if(instrument is None, "Instrument was not found, using the name")
        self.fail_if(conf.KEY_ID not in instrument.keys(), "Instrument has no ID")
        instrument_id = instrument[conf.KEY_ID]
        self.log.debug("Instrument has ID: {}".format(instrument_id))
        instrument = conf.get_instrument(instrument_id)
        self.fail_if(instrument is None, "Instrument was not found, using the ID")
        self.log.debug("Update instrument")
        new_name = "Test instrument new"
        settings[conf.KEY_INSTRUMENT_SETTINGS]["ip_port"] = 18000
        conf.update_instrument(name, new_name, settings)
        self.fail_if(len(conf.get_instruments()) != 1, "The number of instruments is not 1")
        instrument = conf.get_instrument(name)
        self.fail_if(instrument is not None, "Instrument with the old name was found")
        instrument = conf.get_instrument(new_name)
        self.fail_if(instrument is None, "Instrument with the new name was not found")
        self.fail_if(instrument[conf.KEY_ID] != instrument_id, "Instrument ID is not the same")
        self.fail_if(instrument[conf.KEY_SETTINGS][conf.KEY_INSTRUMENT_SETTINGS]["ip_port"] != 18000,
                     "The changed setting was not stored")

    def test_delete_instrument(self):
        conf = Configuration()
        name = "Test instrument"
        settings = {
            conf.KEY_INSTRUMENT_NAME: "Simulator multimeter",
            conf.KEY_INSTRUMENT_SETTINGS: {
                "ip_address": "localhost",
                "ip_port": 17000,
                "rx_timeout": 0.2
            }
        }
        self.log.debug("Add instrument")
        conf.update_instrument(name, name, settings)
        self.fail_if(len(conf.get_instruments()) != 1, "Instrument was not added")
        # Name should be case-insensitive
        conf.delete_instrument("test Instrument")
        self.fail_if(len(conf.get_instruments()) > 0, "Instrument was not deleted")

    def test_add_update_measurement(self):
        conf = Configuration()
        instrument_name = "Test instrument"
        instrument_settings = {
            conf.KEY_INSTRUMENT_NAME: "Simulator multimeter",
            conf.KEY_INSTRUMENT_SETTINGS: {
                "ip_address": "localhost",
                "ip_port": 17000,
                "rx_timeout": 0.2
            }
        }
        self.log.debug("Add instrument")
        conf.update_instrument(instrument_name, instrument_name, instrument_settings)
        self.fail_if(len(conf.get_instruments()) != 1, "Instrument was not added")
        self.log.debug("Add measurement")
        measurement_name = "Test measurement"
        measurement_settings = {
            conf.KEY_INSTRUMENT_ID: "Test instrument",
            conf.KEY_MEASUREMENT: "Get DC voltage",
            conf.KEY_GAIN: 1.0,
            conf.KEY_OFFSET: 0.0
        }
        conf.update_measurement(measurement_name, measurement_name, measurement_settings)
        self.fail_if(len(conf.get_measurements()) != 1, "Measurement was not added")
        measurement = conf.get_measurement(measurement_name)
        self.fail_if(measurement is None, "Measurement was not found")
        self.fail_if(measurement[conf.KEY_SETTINGS][conf.KEY_INSTRUMENT_ID] == instrument_name,
                     "Instrument name was not replaced")
        self.log.debug("Update measurement")
        new_measurement_name = "Test instrument new"
        measurement_settings[conf.KEY_GAIN] = 2.0
        conf.update_measurement(measurement_name, new_measurement_name, measurement_settings)
        self.fail_if(len(conf.get_measurements()) != 1, "The number of measurements is not 1")
        measurement = conf.get_measurement(measurement_name)
        self.fail_if(measurement is not None, "Measurement with the old name was found")
        measurement = conf.get_measurement(new_measurement_name)
        self.fail_if(measurement is None, "Measurement with the new name was not found")
        self.fail_if(measurement[conf.KEY_SETTINGS][conf.KEY_GAIN] != 2.0,
                     "The changed setting was not stored")

    def teardown(self):
        if os.path.isfile(self._filename):
            os.remove(self._filename)


if __name__ == "__main__":

    TestConfiguration().run(True)
