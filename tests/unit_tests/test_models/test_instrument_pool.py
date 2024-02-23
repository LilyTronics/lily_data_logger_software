"""
Test the instrument pool.
"""

from src.models.instrument import Instrument
from src.models.instrument_pool import InstrumentPool
from tests.test_environment.test_configuration import TestConfiguration
from tests.unit_tests.lib.test_suite import TestSuite


class TestInstrumentPool(TestSuite):

    def test_instantiating(self):
        try:
            InstrumentPool()
            self.fail("No run time error was generated, while we expected one")
        except RuntimeError as e:
            self.log.debug("Run time error generated as expected")
            self.log.debug(f"Run time error: {e}")

    def test_add_instrument(self):
        conf = TestConfiguration(True)
        instrument = InstrumentPool.create_instrument(conf.get_instruments()[0])
        self.fail_if(not isinstance(instrument, Instrument),
                     "The created instrument has the wrong class")

    def test_add_instrument_twice(self):
        conf = TestConfiguration(True)
        instrument1 = InstrumentPool.create_instrument(conf.get_instruments()[0])
        self.fail_if(not isinstance(instrument1, Instrument),
                     "The first created instrument has the wrong class")
        instrument2 = InstrumentPool.create_instrument(conf.get_instruments()[0])
        self.fail_if(not isinstance(instrument1, Instrument),
                     "The second created instrument has the wrong class")
        self.fail_if(instrument1 is not instrument2,
                     "The instruments are not the same")

    def test_clear_instruments(self):
        conf = TestConfiguration(True)
        instrument1 = InstrumentPool.create_instrument(conf.get_instruments()[0])
        self.fail_if(not isinstance(instrument1, Instrument),
                     "The first created instrument has the wrong class")
        InstrumentPool.clear_instruments()
        instrument2 = InstrumentPool.create_instrument(conf.get_instruments()[0])
        self.fail_if(not isinstance(instrument1, Instrument),
                     "The second created instrument has the wrong class")
        self.fail_if(instrument1 is not instrument2,
                     "The instruments are not the same")


if __name__ == "__main__":

    import pylint

    TestInstrumentPool().run(True)
    pylint.run_pylint([__file__])
