"""
Configuration model.
"""

import copy
import json
import lily_unit_test
import os


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

    def load_from_file(self, filename):
        self._configuration = copy.deepcopy(self._DEFAULT_CONFIGURATION)
        try:
            with open(filename, 'r') as fp:
                self._configuration = json.load(fp)
        except json.decoder.JSONDecodeError as e:
            raise Exception('Error reading file: {}:\n{}'.format(filename, e))

        self._filename = filename
        self._is_changed = False

    def save_to_file(self, filename):
        with open(filename, 'w') as fp:
            json.dump(self._configuration, fp, indent=2)
        self._filename = filename
        self._is_changed = False

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

    def setup(self):
        self._filename = 'test_config.json'

    def _check_default_values(self, config):
        self.fail_if(config.get_sample_time() != 3, 'The default sample time is incorrect')
        self.fail_if(config.get_end_time() != 60, 'The default end time is incorrect')
        self.fail_if(config.get_continuous_mode(), 'The default continuous mode is incorrect')
        self.fail_if(config.get_instruments() != [], 'The default instruments list is incorrect')
        self.fail_if(config.get_measurements() != [], 'The default measurements list is incorrect')
        self.fail_if(config.get_process_steps() != [], 'The default process steps list is incorrect')
        self.fail_if(config.get_filename() != '<new configuration>', 'The default filename is incorrect')
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

    def test_save_to_load_from_file(self):
        conf = Configuration()
        conf.set_sample_time(10)
        conf.set_end_time(180)
        conf.set_continuous_mode(True)
        conf.save_to_file(self._filename)
        self.fail_if(conf.get_filename() != self._filename, 'The filename is incorrect')

        conf = Configuration()
        conf.load_from_file(self._filename)
        self.fail_if(conf.get_sample_time() != 10, 'The sample time is incorrect')
        self.fail_if(conf.get_end_time() != 180, 'The end time is incorrect')
        self.fail_if(not conf.get_continuous_mode(), 'The continuous mode is incorrect')
        self.fail_if(conf.get_filename() != self._filename, 'The filename is incorrect')
        self.fail_if(conf.is_changed(), 'The changed flag is incorrect')

    def test_load_empty_file(self):
        open(self._filename, 'w').close()
        conf = Configuration()
        try:
            conf.load_from_file(self._filename)
            self.fail('Reading empty file passed, expected an exception')
        except Exception as e:
            self.log.debug('Error message:\n{}'.format(e))
            self.fail_if('Error reading file: {}'.format(self._filename) not in str(e), 'Error message is incorrect')
        self._check_default_values(conf)

    def test_load_invalid_file(self):
        conf = Configuration()
        with open(self._filename, 'w') as fp:
            fp.write('invalid file format\n')
        try:
            conf.load_from_file(self._filename)
            self.fail('Reading empty file passed, expected an exception')
        except Exception as e:
            self.log.debug('Error message:\n{}'.format(e))
            self.fail_if('Error reading file: {}'.format(self._filename) not in str(e), 'Error message is incorrect')
        self._check_default_values(conf)

    def teardown(self):
        if os.path.isfile(self._filename):
            os.remove(self._filename)


if __name__ == '__main__':

    TestConfiguration().run(True)
