"""
Main controller for the application.
"""

import os
import wx

from src.app_data import AppData
from src.controllers.controller_configuration import ControllerConfiguration
from src.models.configuration import Configuration
from src.models.settings import Settings
from src.views.view_logger import ViewLogger
from src.views.view_main import ViewMain
from unit_test.test_suite import TestSuite


class ControllerMain(object):

    def __init__(self, view_title, logger):
        self._logger = logger
        self._logger.info("Load main controller")

        self._settings = Settings()
        self._configuration = Configuration()
        self._elapsed_time = 0

        self._main_view = self._initialize_main_view(view_title)
        self._log_view = None

        self._logger.info("Show main view")
        self._main_view.Show()

        wx.CallAfter(self._update_view_from_configuration)

    ###########
    # Private #
    ###########

    def _initialize_main_view(self, view_title):
        frame = ViewMain(view_title)
        size = self._settings.get_main_window_size()
        if -1 not in size:
            frame.SetSize(size)
        pos = self._settings.get_main_window_position()
        if -1 not in pos:
            frame.SetPosition(pos)
        frame.Maximize(self._settings.get_main_window_maximized())
        frame.Bind(wx.EVT_CLOSE, self._on_view_close)
        frame.Bind(wx.EVT_TOOL, self._on_open_configuration, id=frame.ID_TOOL_OPEN_CONFIGURATION)
        frame.Bind(wx.EVT_TOOL, self._on_save_configuration, id=frame.ID_TOOL_SAVE_CONFIGURATION)
        frame.Bind(wx.EVT_TOOL, self._on_edit_configuration, id=frame.ID_TOOL_EDIT_CONFIGURATION)
        frame.Bind(wx.EVT_TOOL, self._on_show_log, id=frame.ID_TOOL_SHOW_LOG)
        return frame

    def _initialize_log_view(self):
        frame = ViewLogger("Log Messages")
        size = self._settings.get_log_window_size()
        if -1 not in size:
            frame.SetSize(size)
        pos = self._settings.get_log_window_position()
        if -1 not in pos:
            frame.SetPosition(pos)
        frame.Maximize(self._settings.get_log_window_maximized())
        frame.Bind(wx.EVT_CLOSE, self._on_close_log)
        return frame

    def _update_view_from_configuration(self):
        self._main_view.update_configuration_filename(self._configuration.get_filename(),
                                                      self._configuration.is_changed())
        self._main_view.update_configuration_info(self._configuration.get_sample_time(),
                                                  self._configuration.get_end_time(),
                                                  self._configuration.get_continuous_mode())
        self._main_view.update_elapsed_time(self._elapsed_time)

    ##################
    # Event handlers #
    ##################

    def _on_open_configuration(self, event):
        ControllerConfiguration.load_from_file(self._configuration, self._main_view, self._logger)
        self._update_view_from_configuration()
        event.Skip()

    def _on_save_configuration(self, event):
        ControllerConfiguration.save_to_file(self._configuration, self._main_view, self._logger)
        self._update_view_from_configuration()
        event.Skip()

    def _on_edit_configuration(self, event):
        ControllerConfiguration.edit_configuration(self._configuration, self._main_view, self._logger)
        self._update_view_from_configuration()
        event.Skip()

    def _on_show_log(self, event):
        if self._log_view is None:
            self._log_view = self._initialize_log_view()
            self._log_view.show()
        else:
            self._log_view.Raise()
        event.Skip()

    def _on_close_log(self, event):
        self._settings.store_log_window_maximized(self._log_view.IsMaximized())
        if not self._log_view.IsMaximized():
            self._settings.store_log_window_size(*self._log_view.GetSize())
            self._settings.store_log_window_position(*self._log_view.GetPosition())
        self._log_view = None
        event.Skip()

    def _on_view_close(self, event):
        ControllerConfiguration.check_configuration_is_changed(self._configuration, self._main_view, self._logger)
        if self._log_view is not None:
            self._log_view.Close()
        self._settings.store_main_window_maximized(self._main_view.IsMaximized())
        if not self._main_view.IsMaximized():
            self._settings.store_main_window_size(*self._main_view.GetSize())
            self._settings.store_main_window_position(*self._main_view.GetPosition())
        event.Skip()

    ##########
    # Public #
    ##########

    def get_view_main(self):
        return self._main_view


class TestControllerMain(TestSuite):

    _view_main = None

    def setup(self):
        if not os.path.isdir(AppData.USER_FOLDER):
            os.makedirs(AppData.USER_FOLDER)

    def _wait_until_view_available(self):
        self._error = ""
        t = 2
        while t > 0:
            if self._view_main is not None:
                return True
            self.sleep(0.1)
            t -= 0.1
        self._error = "View main did not load"
        return False

    def _show_view_main(self, test_thread):
        self.start_thread(test_thread)
        app = wx.App(redirect=False)
        controller = ControllerMain("ControllerMain Test", self.log)
        self._view_main = controller.get_view_main()
        app.MainLoop()
        self.fail_if(self._error != "", self._error)
        self._view_main = None

    def test_show_view_main(self):
        def _test_show_view_main():
            if self._wait_until_view_available():
                if not self.gui.is_window_available(self._view_main.ID_LIST_INSTRUMENTS):
                    self._error = "The view main was not shown properly"
                self._view_main.Close()

        self._show_view_main(_test_show_view_main)

    def test_configuration_default_values(self):
        def _test_configuration_default_values():
            if self._wait_until_view_available():
                if self.gui.is_window_available(self._view_main.ID_TOTAL_SAMPLES):
                    self.log.debug("Check default settings")
                    value = self.gui.get_value_from_window(self._view_main.ID_SAMPLE_TIME)
                    if value != "00:00:03":
                        self._error = ("The sample time does not have the correct default value '{}', expected '{}'".
                                       format(value, "00:00:03"))
                        return
                    value = self.gui.get_value_from_window(self._view_main.ID_END_TIME)
                    if value != "00:01:00":
                        self._error = ("The end time does not have the correct default value '{}', expected '{}'".
                                       format(value, "00:01:00"))
                        return
                    value = self.gui.get_value_from_window(self._view_main.ID_TOTAL_SAMPLES)
                    if value != "21":
                        self._error = ("The total samples does not have the correct default value '{}', expected '{}'".
                                       format(value, "21"))
                        return
                    self._view_main.Close()

        self._show_view_main(_test_configuration_default_values)

    def test_edit_configuration(self):
        def _test_edit_configuration():
            if self._wait_until_view_available():
                if self.gui.is_window_available(self._view_main.ID_TOTAL_SAMPLES):
                    self.log.debug("Edit settings")
                    # self.gui.click_toolbar_item(self._view_main, self._view_main.ID_TOOL_EDIT_CONFIGURATION)
                    self._view_main.Close()

        self._show_view_main(_test_edit_configuration)


if __name__ == "__main__":

    TestControllerMain().run()
