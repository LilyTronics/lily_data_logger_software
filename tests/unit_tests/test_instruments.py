"""
Test the instruments package.
"""

import glob
import os
import re
import shutil
import tests

from src.app_data import AppData
from src.models.instruments import get_instrument_by_name
from src.models.instruments import get_instrument_names
from tests.test_suite import TestSuite


class TestInstruments(TestSuite):

    _instrument_def = r"\w+ = Instrument\({"
    _n_instruments = 0

    def setup(self):
        n_found = 0
        path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "src", "models", "instruments"))
        self.log.debug("Looking for instruments in: {}".format(path))
        for item in glob.glob(os.path.join(path, "*.py")):
            content = open(item, 'r').read()
            matches = re.findall(self._instrument_def, content)
            if len(matches) == 1:
                n_found += 1
        self._n_instruments = n_found
        self.log.debug("Copy test instrument to user folder")
        shutil.copy2(os.path.join(os.path.dirname(tests.__file__), "test_files", "test_instrument.json"),
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
