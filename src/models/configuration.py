"""
Configuration model.
"""

import copy
import json
import lily_unit_test


class Configuration(object):

    KEY_CONTINUOUS_MODE = 'continuous_mode'
    KEY_END_TIME = 'end_time'
    KEY_GENERAL = 'general'
    KEY_INSTRUMENTS = 'instruments'
    KEY_MEASUREMENTS = 'measurements'
    KEY_PROCESS_STEPS = 'process_steps'
    KEY_SAMPLE_TIME = 'sample_time'

    _DEFAULT_CONFIGURATION = {
        KEY_GENERAL: {
            KEY_SAMPLE_TIME: 3,
            KEY_END_TIME: 60,
            KEY_CONTINUOUS_MODE: False
        },
        KEY_INSTRUMENTS: [],
        KEY_MEASUREMENTS: [],
        KEY_PROCESS_STEPS: []
    }

    def __init__(self):
        self._configuration = copy.deepcopy(self._DEFAULT_CONFIGURATION)
        self._filename = '<new configuration>'
        self._is_changed = False

    def __str__(self): return json.dumps(self._configuration, indent=2)

    def get_filename(self):
        return self._filename

    def is_changed(self):
        return self._is_changed

    ####################
    # General settings #
    ####################

    def get_sample_time(self):
        return self._configuration.get(self.KEY_GENERAL, {}).get(
            self.KEY_SAMPLE_TIME, self._DEFAULT_CONFIGURATION[self.KEY_GENERAL][self.KEY_SAMPLE_TIME])

    def set_sample_time(self, value):
        self._configuration[self.KEY_GENERAL][self.KEY_SAMPLE_TIME] = value
        self._is_changed = True

    def get_end_time(self):
        return self._configuration.get(self.KEY_GENERAL, {}).get(
            self.KEY_END_TIME, self._DEFAULT_CONFIGURATION[self.KEY_GENERAL][self.KEY_END_TIME])

    def set_end_time(self, value):
        self._configuration[self.KEY_GENERAL][self.KEY_END_TIME] = value
        self._is_changed = True

    def get_continuous_mode(self):
        return self._configuration.get(self.KEY_GENERAL, {}).get(
            self.KEY_CONTINUOUS_MODE, self._DEFAULT_CONFIGURATION[self.KEY_GENERAL][self.KEY_CONTINUOUS_MODE])

    def set_continuous_mode(self, value):
        self._configuration[self.KEY_GENERAL][self.KEY_CONTINUOUS_MODE] = value
        self._is_changed = True

    ###############
    # Instruments #
    ###############

    def get_instruments(self):
        return copy.deepcopy(self._configuration.get(self.KEY_INSTRUMENTS,
                                                     self._DEFAULT_CONFIGURATION[self.KEY_INSTRUMENTS]))

    ################
    # Measurements #
    ################

    def get_measurements(self):
        return copy.deepcopy(self._configuration.get(self.KEY_MEASUREMENTS,
                                                     self._DEFAULT_CONFIGURATION[self.KEY_MEASUREMENTS]))

    #################
    # Process steps #
    #################

    def get_process_steps(self):
        return copy.deepcopy(self._configuration.get(self.KEY_PROCESS_STEPS,
                                                     self._DEFAULT_CONFIGURATION[self.KEY_PROCESS_STEPS]))


class TestConfiguration(lily_unit_test.TestSuite):

    def _check_default_values(self, config):
        self.fail_if(config.get_sample_time() != 3, 'The default sample time is incorrect')
        self.fail_if(config.get_end_time() != 60, 'The end time is incorrect')
        self.fail_if(config.get_continuous_mode(), 'The default continuous mode is incorrect')
        self.fail_if(config.get_instruments() != [], 'The instruments list is incorrect')
        self.fail_if(config.get_measurements() != [], 'The measurements list is incorrect')
        self.fail_if(config.get_process_steps() != [], 'The process steps list is incorrect')
        self.fail_if(config.get_filename() != '<new configuration>', 'The filename is incorrect')
        self.fail_if(config.is_changed(), 'The changed flag is incorrect')

    def test_empty_configuration(self):
        conf = Configuration()
        self._check_default_values(conf)

    def test_general_settings(self):
        conf = Configuration()

        current_value = conf.get_sample_time()
        new_value = current_value + 2
        conf.set_sample_time(new_value)
        self.fail_if(conf.get_sample_time() != new_value, 'Failed to store the sample time')
        self.fail_if(not conf.is_changed(), 'The changed flag is incorrect')

        conf._is_changed = False
        current_value = conf.get_end_time()
        new_value = current_value + 2
        conf.set_end_time(new_value)
        self.fail_if(conf.get_end_time() != new_value, 'Failed to store the end time')
        self.fail_if(not conf.is_changed(), 'The changed flag is incorrect')

        conf._is_changed = False
        current_value = conf.get_continuous_mode()
        new_value = not current_value
        conf.set_continuous_mode(new_value)
        self.fail_if(conf.get_continuous_mode() != new_value, 'Failed to store the continuous mode')
        self.fail_if(not conf.is_changed(), 'The changed flag is incorrect')


if __name__ == '__main__':

    TestConfiguration().run()
