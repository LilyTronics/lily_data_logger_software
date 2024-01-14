"""
Instruments package.
"""

import lily_unit_test

from src.models.instruments.simulator_multimeter import simulator_multimeter
from src.models.instruments.simulator_temperature_chamber import simulator_temperature_chamber


_INSTRUMENTS = [
    simulator_multimeter,
    simulator_temperature_chamber
]


def get_instrument_names():
    return sorted(list(map(lambda x: x.get_name(), _INSTRUMENTS)))


def get_instrument_by_name(instrument_name):
    matches = list(filter(lambda x: x.get_name() == instrument_name, _INSTRUMENTS))
    assert len(matches) == 1, 'Instrument with name {} not found'.format(instrument_name)
    return matches[0]


class TestInstruments(lily_unit_test.TestSuite):

    def test_instruments(self):
        for name in get_instrument_names():
            self.log.debug('{:29}: {}'.format(name, get_instrument_by_name(name)))


if __name__ == '__main__':

    TestInstruments().run()
