"""
Create a pool with all required instruments.
Instruments can be used in multiple measurements.
This pool prevents creating multiple instrument objects of the same instrument.
"""

import threading

from src.models.configuration import Configuration
from src.models.instruments import Instruments
from src.models.interface_pool import InterfacePool


class InstrumentPool:

    _INSTRUMENTS = {}
    _LOCK = threading.RLock()

    def __init__(self):
        raise RuntimeError("Creating an instance of this class is not permitted")

    @classmethod
    def create_instrument(cls, instrument_data):
        if not instrument_data[Configuration.KEY_ID] in cls._INSTRUMENTS:
            settings = instrument_data[Configuration.KEY_SETTINGS]
            instrument = Instruments.get_instrument_by_name(
                settings[Configuration.KEY_INSTRUMENT_NAME])
            interface_settings = (instrument.get_interface_settings() |
                                  settings[Configuration.KEY_INSTRUMENT_SETTINGS])
            interface = InterfacePool.create_interface(instrument.get_interface_type(),
                                                       interface_settings)
            instrument.set_interface_object(interface)
            cls._INSTRUMENTS[instrument_data[Configuration.KEY_ID]] = instrument
        return cls._INSTRUMENTS[instrument_data[Configuration.KEY_ID]]


if __name__ == "__main__":

    import pylint
    from tests.unit_tests.test_instrument_pool import TestInstrumentPool

    TestInstrumentPool().run(True)
    pylint.run_pylint([__file__])
