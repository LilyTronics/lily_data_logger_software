"""
Configuration model.
"""

import copy
import json


class Configuration(object):

    KEY_CONTINUOUS_MODE = "continuous_mode"
    KEY_END_TIME = "end_time"
    KEY_GENERAL = "general"
    KEY_INSTRUMENT = "instrument"
    KEY_INSTRUMENT_SETTINGS = "instrument_settings"
    KEY_INSTRUMENTS = "instruments"
    KEY_MEASUREMENTS = "measurements"
    KEY_NAME = "name"
    KEY_PROCESS_STEPS = "process_steps"
    KEY_SAMPLE_TIME = "sample_time"
    KEY_SETTINGS = "settings"

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
        self._filename = "<new configuration>"
        self._is_changed = False

    def __str__(self): return json.dumps(self._configuration, indent=2)

    def load_from_file(self, filename):
        self._configuration = copy.deepcopy(self._DEFAULT_CONFIGURATION)
        try:
            with open(filename, "r") as fp:
                self._configuration = json.load(fp)
        except json.decoder.JSONDecodeError as e:
            raise Exception("Error reading file: {}:\n{}".format(filename, e))

        self._filename = filename
        self._is_changed = False

    def save_to_file(self, filename):
        with open(filename, "w") as fp:
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

    def get_instrument(self, name):
        instruments = self._configuration.get(self.KEY_INSTRUMENTS, self._DEFAULT_CONFIGURATION[self.KEY_INSTRUMENTS])
        matches = list(filter(lambda x: x[self.KEY_NAME] == name, instruments))
        if len(matches) > 0:
            return copy.deepcopy(matches[0])
        return None

    def update_instrument(self, old_name, new_name, settings):
        instruments = self._configuration.get(self.KEY_INSTRUMENTS, self._DEFAULT_CONFIGURATION[self.KEY_INSTRUMENTS])
        matches = list(filter(lambda x: x[self.KEY_NAME] == old_name, instruments))
        if len(matches) == 0:
            instruments.append({
                self.KEY_NAME: new_name,
                self.KEY_SETTINGS: settings
            })
        else:
            matches[0][self.KEY_NAME] = new_name
            matches[0][self.KEY_SETTINGS] = settings

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


if __name__ == "__main__":

    from tests.unit_tests.test_configuration import TestConfiguration

    TestConfiguration().run(True)
