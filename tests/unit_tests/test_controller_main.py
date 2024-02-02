"""
Test for the main controller for the application.
"""

import wx

from src.controllers.controller_main import ControllerMain
from src.models.id_manager import IdManager
from src.models.logger import Logger
from tests.unit_tests.lib.controller_main_test_configuration import ControllerMainTestConfiguration
from tests.unit_tests.lib.test_suite import TestSuite


class TestControllerMain(TestSuite):

    view_main = None

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
                    self.log.debug("Run test function: '{}()'".format(test_function.__name__))
                    self._error = test_function(self)
                else:
                    self._error = "The main view did not appear"
            else:
                self._error = "The main view did not appear"

        self._error = ""
        self.start_thread(_test_thread, (test_function_to_run, ))
        self.test_logger = Logger(redirect_stdout=False)
        app = wx.App(redirect=False)
        controller = ControllerMain("ControllerMain Test", self.test_logger)
        self.view_main = controller.get_view_main()
        app.MainLoop()
        self.fail_if(self._error != "", self._error)
        self.view_main = None

    #######################
    # Test show view main #
    #######################

    def test_show_view_main(self):
        def _test_show_view_main(test_suite):
            test_suite.view_main.Close()
            return ""
        self._show_view_main(_test_show_view_main)

    ######################
    # Test configuration #
    ######################

    def test_configuration_default_values(self):
        self._show_view_main(ControllerMainTestConfiguration.test_configuration_default_values)

    def test_cancel_edit_configuration(self):
        self._show_view_main(ControllerMainTestConfiguration.test_cancel_edit_configuration)

    def test_edit_configuration_fixed_mode(self):
        self._show_view_main(ControllerMainTestConfiguration.test_edit_configuration_fixed_mode)

    def test_edit_configuration_continuous_mode(self):
        self._show_view_main(ControllerMainTestConfiguration.test_edit_configuration_continuous_mode)

    def test_open_configuration(self):
        self._show_view_main(ControllerMainTestConfiguration.test_open_configuration)

    def test_save_configuration(self):
        self._show_view_main(ControllerMainTestConfiguration.test_save_configuration)

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
