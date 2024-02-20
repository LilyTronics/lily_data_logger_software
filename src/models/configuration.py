"""
Configuration model.
"""

import copy
import json
import uuid


class Configuration:

    KEY_CONTINUOUS_MODE = "continuous_mode"
    KEY_END_TIME = "end_time"
    KEY_GAIN = "gain"
    KEY_GENERAL = "general"
    KEY_ID = "id"
    KEY_INSTRUMENT_ID = "instrument_id"
    KEY_INSTRUMENT_NAME = "instrument_name"
    KEY_INSTRUMENT_SETTINGS = "instrument_settings"
    KEY_INSTRUMENTS = "instruments"
    KEY_MEASUREMENT = "measurement"
    KEY_MEASUREMENTS = "measurements"
    KEY_NAME = "name"
    KEY_OFFSET = "offset"
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

    def __str__(self):
        return json.dumps(self._configuration, indent=2)

    ###########
    # Private #
    ###########

    def _find_instrument(self, query):
        # Query can be a name or an ID
        instruments = self._configuration.get(self.KEY_INSTRUMENTS, self._DEFAULT_CONFIGURATION[
            self.KEY_INSTRUMENTS])
        # Try ID first
        matches = list(filter(lambda x: x[self.KEY_ID] == query, instruments))
        if len(matches) == 0:
            # Try name
            matches = list(filter(lambda x: x[self.KEY_NAME].lower() == query.lower(), instruments))
        if len(matches) > 0:
            return matches[0]
        return None

    def _get_id_for_instrument(self, name):
        instrument_id = ""
        instrument = self._find_instrument(name)
        if instrument is not None:
            instrument_id = instrument[self.KEY_ID]
        return instrument_id

    def _find_measurement(self, name):
        measurements = self._configuration.get(self.KEY_MEASUREMENTS,
                                               self._DEFAULT_CONFIGURATION[self.KEY_MEASUREMENTS])
        matches = list(filter(lambda x: x[self.KEY_NAME].lower() == name.lower(), measurements))
        if len(matches) > 0:
            return matches[0]
        return None

    ##########
    # Public #
    ##########

    def load_from_file(self, filename):
        self._configuration = copy.deepcopy(self._DEFAULT_CONFIGURATION)
        try:
            with open(filename, "r", encoding="utf-8") as fp:
                self._configuration = json.load(fp)
        except json.decoder.JSONDecodeError as e:
            raise Exception(f"Error reading file: {filename}:\n{e}") from e
        self._filename = filename
        self._is_changed = False

    def save_to_file(self, filename):
        with open(filename, "w", encoding="utf-8") as fp:
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
            self.KEY_SAMPLE_TIME, self._DEFAULT_CONFIGURATION[self.KEY_GENERAL][
                self.KEY_SAMPLE_TIME])

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
            self.KEY_CONTINUOUS_MODE, self._DEFAULT_CONFIGURATION[self.KEY_GENERAL][
                self.KEY_CONTINUOUS_MODE])

    def set_continuous_mode(self, value):
        self._configuration[self.KEY_GENERAL][self.KEY_CONTINUOUS_MODE] = value
        self._is_changed = True

    ###############
    # Instruments #
    ###############

    def get_instruments(self):
        return copy.deepcopy(self._configuration.get(self.KEY_INSTRUMENTS,
                                                     self._DEFAULT_CONFIGURATION[
                                                         self.KEY_INSTRUMENTS]))

    def get_instrument(self, query):
        match = self._find_instrument(query)
        if match is not None:
            return copy.deepcopy(match)
        return None

    def update_instrument(self, old_name, new_name, settings):
        match = self._find_instrument(old_name)
        if match is None:
            instruments = self._configuration.get(self.KEY_INSTRUMENTS,
                                                  self._DEFAULT_CONFIGURATION[self.KEY_INSTRUMENTS])
            instruments.append({
                self.KEY_ID: str(uuid.uuid4()),
                self.KEY_NAME: new_name,
                self.KEY_SETTINGS: settings
            })
        else:
            match[self.KEY_NAME] = new_name
            match[self.KEY_SETTINGS] = settings
        self._is_changed = True

    def delete_instrument(self, name):
        match = self._find_instrument(name)
        if match is not None:
            instruments = self._configuration.get(self.KEY_INSTRUMENTS,
                                                  self._DEFAULT_CONFIGURATION[self.KEY_INSTRUMENTS])
            instruments.remove(match)
        self._is_changed = True

    def get_used_items_for_instrument(self, name):
        used_items = []
        instrument_id = self._get_id_for_instrument(name)
        used_items.extend(list(filter(lambda x: x[self.KEY_SETTINGS][
                                                    self.KEY_INSTRUMENT_ID] == instrument_id,
                               self.get_measurements())))
        return used_items

    ################
    # Measurements #
    ################

    def get_measurements(self):
        return copy.deepcopy(self._configuration.get(self.KEY_MEASUREMENTS,
                                                     self._DEFAULT_CONFIGURATION[
                                                         self.KEY_MEASUREMENTS]))

    def get_measurement(self, name):
        match = self._find_measurement(name)
        if match is not None:
            return copy.deepcopy(match)
        return None

    def update_measurement(self, old_name, new_name, settings):
        match = self._find_measurement(old_name)
        settings[self.KEY_INSTRUMENT_ID] = self._get_id_for_instrument(settings[
                                                                           self.KEY_INSTRUMENT_ID])
        if match is None:
            measurements = self._configuration.get(self.KEY_MEASUREMENTS,
                                                   self._DEFAULT_CONFIGURATION[
                                                       self.KEY_MEASUREMENTS])
            measurements.append({
                self.KEY_NAME: new_name,
                self.KEY_SETTINGS: settings
            })
        else:
            match[self.KEY_NAME] = new_name
            match[self.KEY_SETTINGS] = settings
        self._is_changed = True

    def delete_measurement(self, name):
        match = self._find_measurement(name)
        if match is not None:
            measurements = self._configuration.get(self.KEY_MEASUREMENTS,
                                                   self._DEFAULT_CONFIGURATION[
                                                       self.KEY_MEASUREMENTS])
            measurements.remove(match)
        self._is_changed = True

    #################
    # Process steps #
    #################

    def get_process_steps(self):
        return copy.deepcopy(self._configuration.get(self.KEY_PROCESS_STEPS,
                                                     self._DEFAULT_CONFIGURATION[
                                                         self.KEY_PROCESS_STEPS]))


if __name__ == "__main__":

    import pylint
    from tests.unit_tests.test_models.test_configuration import TestConfiguration

    TestConfiguration().run(True)
    pylint.run_pylint([__file__])
