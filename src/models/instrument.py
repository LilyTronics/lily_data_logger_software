"""
Instrument model.
"""

import lily_unit_test


class Instrument(object):

    def __init__(self, instrument_definition):
        self._name = instrument_definition.get('name', 'unknown')

    ##########
    # Public #
    ##########

    def get_name(self):
        return self._name


class TestInstrument(lily_unit_test.TestSuite):

    def test_default_values(self):
        instrument = Instrument({})
        self.fail_if(instrument.get_name() != 'unknown',
                     'The default name is not correct {}'.format(instrument.get_name()))


if __name__ == '__main__':

    TestInstrument().run()
