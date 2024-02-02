"""
Instruments package.
"""

import glob
import json
import os

from src.app_data import AppData
from src.models.instrument import Instrument
from src.models.instruments.arduino_uno_daq import arduino_uno_daq
from src.models.instruments.simulator_multimeter import simulator_multimeter


_INSTRUMENTS = [
    arduino_uno_daq
]

_SIMULATORS = [
    simulator_multimeter
]


def get_instrument_names():
    names = sorted(list(map(lambda x: x.get_name(), _get_instruments())))
    names.extend(sorted(list(map(lambda x: x.get_name(), _SIMULATORS))))
    return names


def get_instrument_by_name(instrument_name):
    matches = list(filter(lambda x: x.get_name() == instrument_name, _get_instruments()))
    matches.extend(list(filter(lambda x: x.get_name() == instrument_name, _SIMULATORS)))
    if len(matches) == 1:
        return matches[0]
    return None


def _get_instruments():
    instruments = _INSTRUMENTS.copy()
    for item in glob.glob(os.path.join(AppData.USER_FOLDER, '*.json')):
        try:
            instrument_data = json.load(open(item, 'r'))
            if type(instrument_data) is not dict:
                raise
            for key in [Instrument.KEY_NAME, Instrument.KEY_INFO, Instrument.KEY_INTERFACE,
                        Instrument.KEY_INITIALIZE, Instrument.KEY_CHANNELS]:
                if key not in instrument_data.keys():
                    raise
            instruments.append(Instrument(instrument_data))
        except (Exception, ):
            pass
    return instruments


if __name__ == "__main__":

    from tests.unit_tests.test_instruments import TestInstruments

    TestInstruments().run()
