"""
Test for the controller configuration.
"""

import wx

from src.controllers.controller_edit_instrument import ControllerEditInstrument
from src.models.configuration import Configuration
from src.models.id_manager import IdManager
from tests.unit_tests.lib.test_suite import TestSuite


class TestControllerEditInstrument(TestSuite):

    def setup(self):
        self._app = wx.App(redirect=False)

    def test_add_instrument(self):
        def _test_add_instrument():
            self.gui.wait_until_window_available(IdManager.ID_TEST_CONSOLE)
            self.log.debug("Test no name")
            self.gui.set_value_in_control(IdManager.ID_INSTRUMENT_NAME, "")
            self.gui.click_button(wx.ID_OK)
            if not self.gui.wait_for_dialog(ControllerEditInstrument.get_dialog(), True):
                self._error = "expected dialog did not appear"
            if self._error == "":
                self.gui.send_key_press(self.gui.KEY_ENTER)
                if not self.gui.wait_for_dialog(ControllerEditInstrument.get_dialog(), False):
                    self._error = "dialog did not close"
            if self._error == "":
                self.log.debug("Test no instrument")
                self.gui.set_value_in_control(IdManager.ID_INSTRUMENT_NAME, "Test instrument")
                self.gui.set_value_in_control(IdManager.ID_CMB_INSTRUMENT, "")
                self.gui.click_button(wx.ID_OK)
                if not self.gui.wait_for_dialog(ControllerEditInstrument.get_dialog(), True):
                    self._error = "expected dialog did not appear"
            if self._error == "":
                self.gui.send_key_press(self.gui.KEY_ENTER)
                if not self.gui.wait_for_dialog(ControllerEditInstrument.get_dialog(), False):
                    self._error = "dialog did not close"
            if self._error == "":
                self.log.debug("Test add instrument")
                self.gui.set_value_in_control(IdManager.ID_CMB_INSTRUMENT, "Simulator multimeter")
                self.gui.click_button(wx.ID_OK)
            else:
                self.gui.click_button(wx.ID_CANCEL)

        self._error = ""
        self.start_thread(_test_add_instrument)
        conf = Configuration()
        ControllerEditInstrument.add_instrument(None, conf)
        self.fail_if(self._error != "", self._error)
        self.fail_if(len(conf.get_instruments()) == 0, "Instrument was not added")
        instrument = conf.get_instrument("Test instrument")
        self.fail_if(instrument is None, "Instrument was not added")

    def test_add_same_name(self):
        def _test_add_same_name():
            self.gui.wait_until_window_available(IdManager.ID_TEST_CONSOLE)
            self.log.debug("Add instrument with same name")
            # Use different case, should be case-insensitive
            self.gui.set_value_in_control(IdManager.ID_INSTRUMENT_NAME, "test Instrument")
            self.gui.set_value_in_control(IdManager.ID_CMB_INSTRUMENT, "Simulator multimeter")
            self.gui.click_button(wx.ID_OK)
            if not self.gui.wait_for_dialog(ControllerEditInstrument.get_dialog(), True):
                self._error = "expected dialog did not appear"
            if self._error == "":
                self.gui.send_key_press(self.gui.KEY_ENTER)
                if not self.gui.wait_for_dialog(ControllerEditInstrument.get_dialog(), False):
                    self._error = "dialog did not close"
            self.gui.click_button(wx.ID_CANCEL)

        self._error = ""
        self.start_thread(_test_add_same_name)
        conf = Configuration()
        name = "Test instrument"
        settings = {
            conf.KEY_INSTRUMENT: "Simulator multimeter",
            conf.KEY_INSTRUMENT_SETTINGS: {
                "ip_address": "localhost",
                "ip_port": 17000,
                "rx_timeout": 0.2
            }
        }
        conf.update_instrument(name, name, settings)
        ControllerEditInstrument.add_instrument(None, conf)
        self.fail_if(self._error != "", self._error)

    def teardown(self):
        self._app.MainLoop()


if __name__ == "__main__":

    TestControllerEditInstrument().run()
