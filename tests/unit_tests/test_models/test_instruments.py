"""
Test the instruments package.
"""

import glob
import os
import re
import shutil
import tests

from src.app_data import AppData
from src.models import instruments
from src.models.instruments import Instruments
from tests.unit_tests.lib.test_suite import TestSuite


class TestInstruments(TestSuite):

    _instrument_def = r"\w+ = Instrument\({"
    _n_instruments = 0

    def setup(self):
        # Delete everything in the users folder except the settings and log file
        for item in glob.glob(os.path.join(AppData.USER_FOLDER, "*")):
            if not os.path.basename(item).startswith(AppData.EXE_NAME):
                os.remove(item)
        n_found = 0
        path = os.path.dirname(instruments.__file__)
        self.log.debug(f"Looking for instruments in: {path}")
        for item in glob.glob(os.path.join(path, "*.py")):
            with open(item, "r", encoding="utf-8") as fp:
                content = fp.read()
            matches = re.findall(self._instrument_def, content)
            if len(matches) == 1:
                n_found += 1
        self._n_instruments = n_found
        self.log.debug("Copy test instrument to user folder")
        shutil.copy2(os.path.join(os.path.dirname(tests.__file__),
                                  "test_files", "test_instrument.json"),
                     os.path.join(AppData.USER_FOLDER, "test_instrument.json"))
        self._n_instruments += 1

    def test_instruments(self):
        count = 0
        for name in Instruments.get_instrument_names():
            instrument = Instruments.get_instrument_by_name(name)
            self.log.debug(f"{name:30}: {instrument}")
            self.fail_if(instrument is None, "Instrument not found")
            count += 1
        self.fail_if(count != self._n_instruments,
                     f"The number of instruments is not correct, expecting {self._n_instruments}")
        instrument = Instruments.get_instrument_by_name("Unknown instrument name")
        self.fail_if(instrument is not None, "Unknown instrument name did not return None")

    def teardown(self):
        if os.path.isfile(os.path.join(AppData.USER_FOLDER, "test_instrument.json")):
            os.remove(os.path.join(AppData.USER_FOLDER, "test_instrument.json"))


if __name__ == "__main__":

    TestInstruments().run()
