"""
Our own test suite class derived from the lily-unit-test test suite.
"""

import lily_unit_test

from unit_test.gui_unit_test import GuiUnitTest


class TestSuite(lily_unit_test.TestSuite):
    
    def __init__(self, *args):
        super().__init__(*args)
        self.gui = GuiUnitTest()
