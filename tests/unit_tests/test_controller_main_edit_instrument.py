"""
Configuration test for the main controller.
"""

import os
import tempfile
import wx

from src.models.configuration import Configuration
from src.models.id_manager import IdManager


class TestControllerMainEditInstrument(object):

    @classmethod
    def test_add_instrument(cls, test_suite):

        test_suite.view_main.Close()


if __name__ == "__main__":

    from tests.unit_tests.test_controller_main import TestControllerMain

    TestControllerMain().run()
