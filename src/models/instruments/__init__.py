"""
Instruments package.
"""

import os
import re

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
    instruments = _INSTRUMENTS
    instruments.extend(_get_user_instruments())
    return instruments


def _get_user_instruments():
    instruments = []
    return instruments


class TestInstruments(TestSuite):

    _instrument_def = r'\w+ = Instrument\({'
    _n_instruments = 0

    def setup(self):
        n_found = 0
        path = os.path.dirname(__file__)
        self.log.debug('Looking for instruments in: {}'.format(path))
        for item in os.listdir(path):
            if item.endswith('.py'):
                content = open(item, 'r').read()
                matches = re.findall(self._instrument_def, content)
                if len(matches) == 1:
                    n_found += 1
        self._n_instruments = n_found

    def test_instruments(self):
        count = 0
        for name in get_instrument_names():
            instrument = get_instrument_by_name(name)
            self.log.debug('{:30}: {}'.format(name, instrument))
            self.fail_if(instrument is None, 'Instrument not found')
            count += 1
        self.fail_if(count != self._n_instruments, 'The number of instruments is not correct')
        instrument = get_instrument_by_name('Unknown instrument name')
        self.fail_if(instrument is not None, 'Unknown instrument name did not return None')


if __name__ == '__main__':

    TestInstruments().run()
