"""
Test the check instruments' dialog.
"""

import wx

from src.controllers.controller_check_instruments import ControllerCheckInstruments
from src.models.configuration import Configuration
from src.models.id_manager import IdManager
from tests.unit_tests.lib.test_suite import TestSuite


class TestControllerCheckInstrument(TestSuite):

    _app = None
    _error = ""

    def setup(self):
        self._app = wx.App(redirect=False)

    def test_check_instruments(self):
        def _test_check_instruments():
            if not self.gui.wait_until_window_available(IdManager.ID_BTN_CHECK):
                self._error = "The view check instruments did not appear"
            else:
                self.gui.click_button(IdManager.ID_BTN_CHECK)
                view = self.gui.get_window(IdManager.ID_BTN_CHECK).GetParent()
                if not self.gui.wait_for_dialog(view, True):
                    self._error = "The progress dialog did not appear"
                elif not self.gui.wait_for_dialog(view, False):
                    self._error = "The progress dialog did not close"
                view.Close()

        self._error = ""
        t = self.start_thread(_test_check_instruments)
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
        ControllerCheckInstruments(None, conf)
        self.wait_for(t.is_alive, False, 10, 0.1)
        self.fail_if(self._error != "", self._error)

    def teardown(self):
        self._app.MainLoop()


if __name__ == "__main__":

    import pylint

    TestControllerCheckInstrument().run(True)
    pylint.run_pylint([__file__])
