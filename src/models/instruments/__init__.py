"""
Instruments package.
"""

from src.models.instruments.simulator_multimeter import simulator_multimeter
from src.models.instruments.simulator_temperature_chamber import simulator_temperature_chamber
from unit_test.test_suite import TestSuite


_INSTRUMENTS = [
    simulator_multimeter,
    simulator_temperature_chamber
]


def get_instrument_names():
    return sorted(list(map(lambda x: x.get_name(), _INSTRUMENTS)))


def get_instrument_by_name(instrument_name):
    matches = list(filter(lambda x: x.get_name() == instrument_name, _INSTRUMENTS))
    if len(matches) == 1:
        return matches[0]
    return None


class TestInstruments(TestSuite):

    def test_instruments(self):
        for name in get_instrument_names():
            self.log.debug('{:29}: {}'.format(name, get_instrument_by_name(name)))
        instrument = get_instrument_by_name('Unknown instrument name')
        self.fail_if(instrument is not None, 'Unknown instrument name did not return None')


if __name__ == '__main__':

    TestInstruments().run()
