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
        result = ""
        test_suite.gui.click_button(IdManager.ID_BTN_ADD_INSTRUMENT)
        if not test_suite.gui.wait_until_window_available(IdManager.ID_TEST_CONSOLE):
            result += "\nThe edit instrument dialog did not appear"
        else:
            test_suite.log.debug("Add instrument")
            test_suite.gui.set_value_in_control(IdManager.ID_INSTRUMENT_NAME, "Test instrument")
            test_suite.gui.set_value_in_control(IdManager.ID_CMB_INSTRUMENT, "Simulator multimeter")
            test_suite.gui.click_button(wx.ID_OK)
            test_suite.log.debug("Check if instrument is in the list")
            list_control = test_suite.gui.get_window(IdManager.ID_LIST_INSTRUMENTS)
            test_suite.wait_for(list_control.GetItemCount, 1, 1, 0.1)
            if list_control.GetItemCount() < 1:
                result += "The instrument is not in the list"
            elif list_control.GetItemText(0) != "Test instrument":
                result += "Wrong instrument name in the list"
        result += test_suite.close_view_main(True)
        return result


if __name__ == "__main__":

    from tests.unit_tests.test_controller_main import TestControllerMain

    TestControllerMain().run()
