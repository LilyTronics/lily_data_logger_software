"""
Our own test suite class derived from the lily-unit-test test suite.
"""

import lily_unit_test
import os

from src.app_data import AppData
from tests.gui_unit_test import GuiUnitTest


class TestSuite(lily_unit_test.TestSuite):
    
    def __init__(self, *args):
        super().__init__(*args)
        self.gui = GuiUnitTest()
        self.configuration_test_filename = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                                                        "test_files", "test_configuration.json"))
        if not os.path.isdir(AppData.USER_FOLDER):
            os.makedirs(AppData.USER_FOLDER)


if __name__ == "__main__":

    ts = TestSuite()
    print("Configuration test filename:", ts.configuration_test_filename)
