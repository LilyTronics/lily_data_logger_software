"""
Base class for all main controller tests.
"""

import wx

from src.controllers.controller_main import ControllerMain
from src.models.id_manager import IdManager
from src.models.logger import Logger
from tests.unit_tests.lib.test_suite import TestSuite


class TestControllerMain(TestSuite):

    view_main = None
    logger = None
    _error = ""
    _thread_time_out = 30

    def _wait_until_view_main_available(self):
        self._error = ""
        t = 2
        while t > 0:
            if self.view_main is not None:
                return True
            self.sleep(0.1)
            t -= 0.1
        self._error = "View main did not load"
        return False

    def show_view_main(self, test_function_to_run, load_test_configuration=False):
        def _test_thread(test_function):
            if self._wait_until_view_main_available():
                if self.gui.is_window_available(IdManager.ID_LABEL_ELAPSED_TIME):
                    self._error = test_function()
                else:
                    self._error = "The main view did not appear"
            else:
                self._error = "The main view did not appear"

        self._error = ""
        t = self.start_thread(_test_thread, (test_function_to_run, ))
        self.logger = Logger(redirect_stdout=False)
        app = self.gui.get_wx_app()
        controller = ControllerMain("ControllerMain Test", self.logger, load_test_configuration)
        self.view_main = controller.get_view_main()
        app.MainLoop()
        self.wait_for(t.is_alive, False, self._thread_time_out, 0.1)
        self.view_main = None
        self.gui.destroy_wx_app()
        self.fail_if(self._error != "", self._error.strip())

    def close_view_main(self, expect_dialog):
        def _close_dialog():
            self.gui.send_key_press(self.gui.KEY_TAB)
            self.gui.send_key_press(self.gui.KEY_ENTER)
            if not self.gui.wait_for_dialog(self.view_main, False):
                return "\nChanged configuration dialog did not close"
            return ""

        result = ""
        self.gui.post_event(self.view_main, wx.wxEVT_CLOSE_WINDOW, self.view_main.GetId())
        self.log.debug("Check if there is a configuration changed dialog")
        if self.gui.wait_for_dialog(self.view_main) == expect_dialog:
            if expect_dialog:
                result += _close_dialog()
            else:
                self.log.debug("No configuration changed dialog appeared as expected")
        else:
            if expect_dialog:
                result += "\nConfiguration changed dialog did not appear while we expected one"
            else:
                result += "\nConfiguration changed dialog did appear while we did not expect it"
                result += _close_dialog()

        return result

    def test_show_view_main(self):
        def _test_show_view_main():
            return ""

        self.show_view_main(_test_show_view_main, True)


if __name__ == "__main__":

    import pylint

    TestControllerMain().run(True)
    pylint.run_pylint([__file__])
