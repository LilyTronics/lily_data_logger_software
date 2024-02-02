"""
Main controller for the application.
"""

import os
import tempfile
import wx

from src.app_data import AppData
from src.controllers.controller_configuration import ControllerConfiguration
from src.models.configuration import Configuration
from src.models.id_manager import IdManager
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
        frame.Bind(wx.EVT_TOOL, self._on_open_configuration, id=IdManager.ID_TOOL_OPEN_CONFIGURATION)
        frame.Bind(wx.EVT_TOOL, self._on_save_configuration, id=IdManager.ID_TOOL_SAVE_CONFIGURATION)
        frame.Bind(wx.EVT_TOOL, self._on_edit_configuration, id=IdManager.ID_TOOL_EDIT_CONFIGURATION)
        frame.Bind(wx.EVT_TOOL, self._on_show_log, id=IdManager.ID_TOOL_SHOW_LOG)
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

    @staticmethod
    def setup():
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
        self._error = ""
        self.start_thread(test_thread)
        app = wx.App(redirect=False)
        controller = ControllerMain("ControllerMain Test", self.log)
        self._view_main = controller.get_view_main()
        app.MainLoop()
        self.fail_if(self._error != "", self._error)
        self._view_main = None

    def _check_configuration_values(self, sample_time, end_time, total_samples):
        wx.Yield()
        self.sleep(0.2)
        value = self.gui.get_value_from_window(IdManager.ID_LABEL_SAMPLE_TIME)
        if value != sample_time:
            self._error = ("The sample time does not have the correct value: '{}', expected '{}'".
                           format(value, sample_time))
            return
        value = self.gui.get_value_from_window(IdManager.ID_LABEL_END_TIME)
        if value != end_time:
            self._error = ("The end time does not have the correct value: '{}', expected '{}'".
                           format(value, end_time))
            return
        # When continuous mode, total samples is not interesting
        if total_samples is not None:
            value = self.gui.get_value_from_window(IdManager.ID_LABEL_TOTAL_SAMPLES)
            if value != total_samples:
                self._error = ("The total samples does not have the correct value: '{}', expected '{}'".
                               format(value, total_samples))
                return

    def test_show_view_main(self):
        def _test_show_view_main():
            if self._wait_until_view_available():
                if not self.gui.is_window_available(IdManager.ID_LIST_INSTRUMENTS):
                    self._error = "The view main was not shown properly"
                self._view_main.Close()

        self._show_view_main(_test_show_view_main)

    def test_configuration_default_values(self):
        def _test_configuration_default_values():
            if self._wait_until_view_available():
                if self.gui.is_window_available(IdManager.ID_LABEL_TOTAL_SAMPLES):
                    self.log.debug("Check default configuration")
                    self._check_configuration_values("00:00:03", "00:01:00", "21")
                    self._view_main.Close()

        self._show_view_main(_test_configuration_default_values)

    def test_cancel_edit_configuration(self):
        def _test_cancel_edit_configuration():
            if self._wait_until_view_available():
                if self.gui.is_window_available(IdManager.ID_LABEL_TOTAL_SAMPLES):
                    self.log.debug("Edit configuration")
                    self.gui.click_toolbar_item(self._view_main, IdManager.ID_TOOL_EDIT_CONFIGURATION)
                    if self.gui.wait_until_window_available(IdManager.ID_END_TIME):
                        self.gui.set_value_in_control(IdManager.ID_SAMPLE_TIME, "5")
                        self.gui.set_value_in_control(IdManager.ID_END_TIME, "3")
                        self.gui.click_button(wx.ID_CANCEL)
                        self._check_configuration_values("00:00:03", "00:01:00", "21")
                    self._view_main.Close()

        self._show_view_main(_test_cancel_edit_configuration)

    def test_edit_configuration_fixed_mode(self):
        def _test_edit_configuration_fixed_mode():
            if self._wait_until_view_available():
                if self.gui.is_window_available(IdManager.ID_LABEL_TOTAL_SAMPLES):
                    self.log.debug("Edit configuration")
                    self.gui.click_toolbar_item(self._view_main, IdManager.ID_TOOL_EDIT_CONFIGURATION)
                    if self.gui.wait_until_window_available(IdManager.ID_END_TIME):
                        self.gui.set_value_in_control(IdManager.ID_SAMPLE_TIME, "5")
                        self.gui.set_value_in_control(IdManager.ID_END_TIME, "3")
                        self.gui.click_button(wx.ID_OK)
                        self._check_configuration_values("00:00:05", "00:03:00", "37")
                    self.gui.post_event(self._view_main, wx.wxEVT_CLOSE_WINDOW, self._view_main.GetId())
                    self.log.debug("Check for configuration changed dialog")
                    if self.gui.wait_for_dialog(self._view_main):
                        self.gui.send_key_press(self.gui.KEY_TAB)
                        self.gui.send_key_press(self.gui.KEY_ENTER)
                        if not self.gui.wait_for_dialog(self._view_main, False):
                            self.fail("Changed configuration dialog did not close")
                    else:
                        self.fail("No changed configuration dialog appeared")

        self._show_view_main(_test_edit_configuration_fixed_mode)

    def test_edit_configuration_continuous_mode(self):
        def _test_edit_configuration_continuous_mode():
            if self._wait_until_view_available():
                if self.gui.is_window_available(IdManager.ID_LABEL_TOTAL_SAMPLES):
                    self.log.debug("Edit configuration")
                    self.gui.click_toolbar_item(self._view_main, IdManager.ID_TOOL_EDIT_CONFIGURATION)
                    if self.gui.wait_until_window_available(IdManager.ID_END_TIME):
                        self.gui.set_value_in_control(IdManager.ID_SAMPLE_TIME, "5")
                        self.gui.set_value_in_control(IdManager.ID_END_TIME, "3")
                        self.gui.select_radio_button(IdManager.ID_CONTINUOUS)
                        self.gui.click_button(wx.ID_OK)
                        self._check_configuration_values("00:00:05", "Continuous mode", None)
                    self.gui.post_event(self._view_main, wx.wxEVT_CLOSE_WINDOW, self._view_main.GetId())
                    self.log.debug("Check for configuration changed dialog")
                    if self.gui.wait_for_dialog(self._view_main):
                        self.gui.send_key_press(self.gui.KEY_TAB)
                        self.gui.send_key_press(self.gui.KEY_ENTER)
                        if not self.gui.wait_for_dialog(self._view_main, False):
                            self.fail("Changed configuration dialog did not close")
                    else:
                        self.fail("No changed configuration dialog appeared")

        self._show_view_main(_test_edit_configuration_continuous_mode)

    def test_open_configuration(self):
        def _test_open_configuration():
            if self._wait_until_view_available():
                if self.gui.is_window_available(IdManager.ID_LABEL_TOTAL_SAMPLES):
                    self.log.debug("Open configuration from file: {}".format(self.configuration_test_filename))
                    self.gui.click_toolbar_item(self._view_main, IdManager.ID_TOOL_OPEN_CONFIGURATION)
                    self.log.debug("Check for open configuration dialog")
                    if self.gui.wait_for_dialog(self._view_main):
                        self.gui.send_text(self.configuration_test_filename)
                        self.gui.send_key_press(self.gui.KEY_ENTER)
                        self._check_configuration_values("00:00:04", "00:05:00", "76")
                    else:
                        self.fail("No open configuration file dialog appeared")
                    self._view_main.Close()

        self._show_view_main(_test_open_configuration)

    def test_save_configuration(self):
        def _test_save_configuration():
            if self._wait_until_view_available():
                if self.gui.is_window_available(IdManager.ID_LABEL_TOTAL_SAMPLES):
                    self.log.debug("Change configuration before saving")
                    self.gui.click_toolbar_item(self._view_main, IdManager.ID_TOOL_EDIT_CONFIGURATION)
                    if self.gui.wait_until_window_available(IdManager.ID_END_TIME):
                        self.gui.set_value_in_control(IdManager.ID_SAMPLE_TIME, "5")
                        self.gui.set_value_in_control(IdManager.ID_END_TIME, "3")
                        self.gui.click_button(wx.ID_OK)
                        self._check_configuration_values("00:00:05", "00:03:00", "37")
                        self.gui.click_toolbar_item(self._view_main, IdManager.ID_TOOL_SAVE_CONFIGURATION)
                        self.log.debug("Check for save configuration dialog")
                        if self.gui.wait_for_dialog(self._view_main):
                            self.gui.send_text(self._filename)
                            self.gui.send_key_press(self.gui.KEY_ENTER)
                            # We need some time to save
                            self.sleep(0.2)
                        else:
                            self.fail("No save configuration file dialog appeared")
                        self._view_main.Close()

        self._filename = tempfile.mktemp(suffix=".json")
        self._show_view_main(_test_save_configuration)

        self.log.debug("Check values in the saved configuration")
        conf = Configuration()
        conf.load_from_file(self._filename)
        self.fail_if(conf.get_sample_time() != 5,
                     "Sample time was not saved correct: {}, expected 5".format(conf.get_sample_time()))
        self.fail_if(conf.get_end_time() != 180,
                     "End time was not saved correct: {}, expected 180".format(conf.get_end_time()))
        self.fail_if(conf.get_continuous_mode(),
                     "Continuous mode was not saved correct: {}, expected False".format(conf.get_continuous_mode()))

        if os.path.isfile(self._filename):
            os.remove(self._filename)


if __name__ == "__main__":

    TestControllerMain().run()
