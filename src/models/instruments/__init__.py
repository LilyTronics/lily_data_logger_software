"""
Instruments package.
"""

from src.models.instruments import simulator_multimeter
from src.models.instruments import simulator_temperature_chamber


_INSTRUMENTS = [
    simulator_multimeter.INSTRUMENT,
    simulator_temperature_chamber.INSTRUMENT
]


def get_instrument_names():
    return sorted(list(map(lambda x: x['name'], _INSTRUMENTS)))


def get_instrument_by_name(instrument_name):
    matches = list(filter(lambda x: x['name'] == instrument_name, _INSTRUMENTS))
    assert len(matches) == 1, 'Instrument with name {} not found'.format(instrument_name)
    return matches[0]


if __name__ == '__main__':

    for name in get_instrument_names():
        print('{:29}: {}'.format(name, get_instrument_by_name(name)))
