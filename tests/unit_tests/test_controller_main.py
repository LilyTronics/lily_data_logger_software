"""
Test for the main controller for the application.
"""

import wx

from src.controllers.controller_main import ControllerMain
from src.models.id_manager import IdManager
from src.models.logger import Logger
from tests.unit_tests.test_controller_main_configuration import TestControllerMainConfiguration
from tests.unit_tests.test_controller_main_edit_instrument import TestControllerMainEditInstrument
from tests.unit_tests.lib.test_suite import TestSuite


class TestControllerMain(TestSuite):

    view_main = None

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

    def _show_view_main(self, test_function_to_run):
        def _test_thread(test_function):
            if self._wait_until_view_main_available():
                if self.gui.is_window_available(IdManager.ID_LABEL_ELAPSED_TIME):
                    self._error = test_function(self)
                else:
                    self._error = "The main view did not appear"
            else:
                self._error = "The main view did not appear"

        self._error = ""
        t = self.start_thread(_test_thread, (test_function_to_run, ))
        self.test_logger = Logger(redirect_stdout=False)
        app = wx.App(redirect=False)
        controller = ControllerMain("ControllerMain Test", self.test_logger)
        self.view_main = controller.get_view_main()
        app.MainLoop()
        self.wait_for(t.is_alive, False, self._thread_time_out, 0.1)
        self.fail_if(self._error != "", self._error.strip())
        self.view_main = None

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

    #######################
    # Test show view main #
    #######################

    def test_show_view_main(self):
        def _test_show_view_main(test_suite):
            return test_suite.close_view_main(False)
        self._show_view_main(_test_show_view_main)

    ######################
    # Test configuration #
    ######################

    def test_configuration_default_values(self):
        self._show_view_main(TestControllerMainConfiguration.test_configuration_default_values)

    def test_cancel_edit_configuration(self):
        self._show_view_main(TestControllerMainConfiguration.test_cancel_edit_configuration)

    def test_edit_configuration_fixed_mode(self):
        self._show_view_main(TestControllerMainConfiguration.test_edit_configuration_fixed_mode)

    def test_edit_configuration_continuous_mode(self):
        self._show_view_main(TestControllerMainConfiguration.test_edit_configuration_continuous_mode)

    def test_open_configuration(self):
        self._show_view_main(TestControllerMainConfiguration.test_open_configuration)

    def test_save_configuration(self):
        self._show_view_main(TestControllerMainConfiguration.test_save_configuration)

    ########################
    # Test edit instrument #
    ########################

    def test_add_instrument(self):
        self._show_view_main(TestControllerMainEditInstrument.test_add_instrument)

    ###################
    # Test log viewer #
    ###################

    def test_log_viewer(self):
        def _has_log_messages():
            return self.gui.get_value_from_window(IdManager.ID_LOG_MESSAGES) != ""

        def _get_log_view_object():
            matches = list(filter(lambda x: x.__class__.__name__ == "ViewLogger", wx.GetTopLevelWindows()))
            if len(matches) == 1:
                return matches[0]
            return None

        def _test_log_viewer(test_suite):
            result = ""
            test_suite.log.debug("Open log view")
            test_suite.gui.click_toolbar_item(test_suite.view_main, IdManager.ID_TOOL_SHOW_LOG)
            if test_suite.gui.wait_until_window_available(IdManager.ID_LOG_MESSAGES):
                test_suite.test_logger.debug("This is a test message")
                # The log view has a 300ms update rate
                test_suite.log.debug("Check log messages")
                test_suite.wait_for(_has_log_messages, True, 1, 0.2)
                messages = test_suite.gui.get_value_from_window(IdManager.ID_LOG_MESSAGES)
                if " | DEBUG  | This is a test message" not in messages:
                    result = "The log message was not shown in the log window"
                log_view = _get_log_view_object()
                if log_view is None:
                    result = "Log window object not found"
                else:
                    test_suite.log.debug("Close log view")
                    log_view.Close()
                    if not test_suite.wait_for(_get_log_view_object, None, 1, 0.1):
                        result = "The log window did not close"
                    else:
                        test_suite.log.debug("Open log view again")
                        test_suite.gui.click_toolbar_item(test_suite.view_main, IdManager.ID_TOOL_SHOW_LOG)
                        if not test_suite.gui.wait_until_window_available(IdManager.ID_LOG_MESSAGES):
                            result = "The log window did not appear"
            else:
                result = "The log window did not appear"
            test_suite.log.debug("Close log view by closing the main view")
            test_suite.view_main.Close()
            if not test_suite.wait_for(_get_log_view_object, None, 1, 0.1):
                result = "The log window did not close"
            return result

        self._show_view_main(_test_log_viewer)


if __name__ == "__main__":

    TestControllerMain().run()
