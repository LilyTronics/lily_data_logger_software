"""
Instruments package.
"""

import glob
import json
import os
import re
import shutil
import unit_test

from src.app_data import AppData
from src.models.instrument import Instrument
from src.models.instruments.power_supply_tti_pl303qmd_p import tti_pl303qmd_p
from src.models.instruments.simulator_multimeter import simulator_multimeter
from src.models.instruments.simulator_temperature_chamber import simulator_temperature_chamber
from unit_test.test_suite import TestSuite


_INSTRUMENTS = [
    tti_pl303qmd_p
]

_SIMULATORS = [
    simulator_multimeter,
    simulator_temperature_chamber
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


class TestInstruments(TestSuite):

    _instrument_def = r"\w+ = Instrument\({"
    _n_instruments = 0

    def setup(self):
        n_found = 0
        path = os.path.dirname(__file__)
        self.log.debug("Looking for instruments in: {}".format(path))
        for item in glob.glob(os.path.join(path, "*.py")):
            content = open(item, 'r').read()
            matches = re.findall(self._instrument_def, content)
            if len(matches) == 1:
                n_found += 1
        self._n_instruments = n_found
        self.log.debug("Copy test instrument to user folder")
        shutil.copy2(os.path.join(os.path.dirname(unit_test.__file__), "test_files", "test_instrument.json"),
                     os.path.join(AppData.USER_FOLDER, "test_instrument.json"))
        self._n_instruments += 1

    def test_instruments(self):
        count = 0
        for name in get_instrument_names():
            instrument = get_instrument_by_name(name)
            self.log.debug("{:30}: {}".format(name, instrument))
            self.fail_if(instrument is None, "Instrument not found")
            count += 1
        self.fail_if(count != self._n_instruments, "The number of instruments is not correct, expecting {}".format(
            self._n_instruments))
        instrument = get_instrument_by_name("Unknown instrument name")
        self.fail_if(instrument is not None, "Unknown instrument name did not return None")

    @staticmethod
    def teardown():
        if os.path.isfile(os.path.join(AppData.USER_FOLDER, "test_instrument.json")):
            os.remove(os.path.join(AppData.USER_FOLDER, "test_instrument.json"))


if __name__ == "__main__":

    TestInstruments().run()
