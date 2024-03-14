"""
Instruments package.
"""

import glob
import json
import os

from src.app_data import AppData
from src.models.instrument import Instrument
from src.models.instruments.arduino_daq import arduino_daq
from src.models.instruments.simulator_multimeter import simulator_multimeter
from src.models.instruments.simulator_temperature_meter import simulator_temperature_meter


class Instruments:

    _INSTRUMENTS = [
        arduino_daq
    ]

    _SIMULATORS = [
        simulator_multimeter,
        simulator_temperature_meter
    ]

    ##########
    # Public #
    ##########

    @classmethod
    def get_instrument_names(cls):
        names = sorted(list(map(lambda x: x.get_name(), cls._get_instruments())))
        names.extend(sorted(list(map(lambda x: x.get_name(), cls._SIMULATORS))))
        return names

    @classmethod
    def get_instrument_by_name(cls, instrument_name):
        matches = list(filter(lambda x: x.get_name() == instrument_name, cls._get_instruments()))
        matches.extend(list(filter(lambda x: x.get_name() == instrument_name, cls._SIMULATORS)))
        if len(matches) == 1:
            return matches[0]
        return None

    ###########
    # Private #
    ###########

    @classmethod
    def _get_instruments(cls):
        instruments = cls._INSTRUMENTS.copy()
        for item in glob.glob(os.path.join(AppData.USER_FOLDER, '*.json')):
            try:
                with open(item, "r", encoding="utf-8") as fp:
                    instrument_data = json.load(fp)
                if isinstance(instrument_data, dict):
                    has_valid_keys = True
                    for key in [Instrument.KEY_NAME, Instrument.KEY_INFO, Instrument.KEY_INTERFACE,
                                Instrument.KEY_INITIALIZE, Instrument.KEY_CHANNELS]:
                        if key not in instrument_data.keys():
                            has_valid_keys = False
                    if has_valid_keys:
                        instruments.append(Instrument(instrument_data))
            except Exception as e:
                print(f"Error reading file '{item}': {e}")
        return instruments


if __name__ == "__main__":

    from tests.unit_tests.test_models.test_instruments import TestInstruments

    TestInstruments().run()
