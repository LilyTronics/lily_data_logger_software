"""
Test for the controller configuration.
"""

import wx

from src.controllers.controller_edit_instrument import ControllerEditInstrument
from src.models.configuration import Configuration
from src.models.id_manager import IdManager
from tests.unit_tests.lib.test_suite import TestSuite


class TestControllerEditInstrument(TestSuite):

    _app = None
    _error = ""

    def setup(self):
        self._app = self.gui.get_wx_app()

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
        ControllerEditInstrument.edit_instrument(None, conf, "")
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
            conf.KEY_INSTRUMENT_NAME: "Simulator multimeter",
            conf.KEY_INSTRUMENT_SETTINGS: {
                "ip_address": "localhost",
                "ip_port": 17000,
                "rx_timeout": 0.2
            }
        }
        conf.update_instrument(name, name, settings)
        ControllerEditInstrument.edit_instrument(None, conf, "")
        self.fail_if(self._error != "", self._error)

    def test_edit_instrument(self):
        def _test_edit_instrument():
            self.gui.wait_until_window_available(IdManager.ID_TEST_CONSOLE)
            self.log.debug("Change name")
            self.gui.set_value_in_control(IdManager.ID_INSTRUMENT_NAME, "Test instrument edit")
            settings_controls = ControllerEditInstrument.get_dialog().get_settings_controls()
            self.log.debug("Change settings")
            settings_controls["ip_address"].SetValue("5.6.7.8")
            settings_controls["ip_port"].SetValue("19000")
            settings_controls["rx_timeout"].SetValue("1")
            self.gui.click_button(wx.ID_OK)

        self._error = ""
        self.start_thread(_test_edit_instrument)
        conf = Configuration()
        name = "Test instrument"
        settings = {
            conf.KEY_INSTRUMENT_NAME: "Simulator multimeter",
            conf.KEY_INSTRUMENT_SETTINGS: {
                "ip_address": "1.2.3.4",
                "ip_port": 18000,
                "rx_timeout": 0.5
            }
        }
        conf.update_instrument(name, name, settings)
        ControllerEditInstrument.edit_instrument(None, conf, name)
        instrument = conf.get_instrument("Test instrument edit")
        self.fail_if(instrument is None, "The name did not change")
        settings = instrument[conf.KEY_SETTINGS][conf.KEY_INSTRUMENT_SETTINGS]
        self.fail_if(settings["ip_address"] != "5.6.7.8", "The IP address did not change")
        self.fail_if(settings["ip_port"] != "19000", "The port did not change")
        self.fail_if(settings["rx_timeout"] != "1", "The RX timeout did not change")

    def teardown(self):
        self._app.MainLoop()
        self.gui.destroy_wx_app()
        del self._app


if __name__ == "__main__":

    import pylint

    TestControllerEditInstrument().run(True)
    pylint.run_pylint([__file__])
