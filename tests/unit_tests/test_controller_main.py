"""
Test for the main controller for the application.
"""

import wx

from src.controllers.controller_main import ControllerMain
from src.models.id_manager import IdManager
from tests.unit_tests.lib.controller_main_test_configuration import ControllerMainTestConfiguration
from tests.test_suite import TestSuite


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
        app = wx.App(redirect=False)
        controller = ControllerMain("ControllerMain Test", self.log)
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


if __name__ == "__main__":

    TestControllerMain().run()
