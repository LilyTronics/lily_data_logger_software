"""
Our own test suite class derived from the lily-unit-test test suite.
"""

import os
import lily_unit_test

from src.app_data import AppData
from tests.unit_tests.lib.gui_unit_test import GuiUnitTest


class TestSuite(lily_unit_test.TestSuite):

    def __init__(self, *args):
        super().__init__(*args)
        self.gui = GuiUnitTest()
        self.configuration_test_filename = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                                                        "..", "..",
                                                                        "test_files",
                                                                        "test_configuration.json"))
        if not os.path.isdir(AppData.USER_FOLDER):
            os.makedirs(AppData.USER_FOLDER)


if __name__ == "__main__":

    import pylint

    ts = TestSuite()
    print("Configuration test filename:", ts.configuration_test_filename)
    pylint.run_pylint([__file__])
