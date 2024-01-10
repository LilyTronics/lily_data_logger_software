"""
Main controller for the application.
"""

import wx

from src.models.configuration import Configuration
from src.models.settings import Settings
from src.views.view_logger import ViewLogger
from src.views.view_edit_configuration import ViewEditConfiguration
from src.views.view_main import ViewMain


class ControllerMain(object):

    def __init__(self, view_title, logger):
        self._logger = logger
        self._logger.debug('Load main controller')
        self._settings = Settings()
        self._view = ViewMain(view_title)
        size = self._settings.get_main_window_size()
        if -1 not in size:
            self._view.SetSize(size)
        pos = self._settings.get_main_window_position()
        if -1 not in pos:
            self._view.SetPosition(pos)
        self._view.Maximize(self._settings.get_main_window_maximized())
        self._view.Bind(wx.EVT_CLOSE, self._on_view_close)
        self._view.Bind(wx.EVT_TOOL, self._on_edit_configuration, id=self._view.ID_TOOL_EDIT_CONFIGURATION)
        self._view.Bind(wx.EVT_TOOL, self._on_show_log, id=self._view.ID_TOOL_SHOW_LOG)
        self._configuration = Configuration()
        self._elapsed_time = 0
        self._log_view = None

        wx.CallAfter(self._update_view_from_configuration)

    ##################
    # Event handlers #
    ##################

    def _on_edit_configuration(self, event):
        dlg = ViewEditConfiguration(self._view)
        dlg.set_sample_time(self._configuration.get_sample_time())
        dlg.set_end_time(self._configuration.get_end_time())
        dlg.set_continuous_mode(self._configuration.get_continuous_mode())
        if dlg.ShowModal() == wx.ID_OK:
            self._configuration.set_sample_time(dlg.get_sample_time())
            self._configuration.set_end_time(dlg.get_end_time())
            self._configuration.set_continuous_mode(dlg.get_continuous_mode())
            self._update_view_from_configuration()
        dlg.Destroy()
        event.Skip()

    def _on_show_log(self, event):
        self._show_log()
        event.Skip()

    def _on_close_log(self, event):
        self._settings.store_log_window_maximized(self._log_view.IsMaximized())
        if not self._log_view.IsMaximized():
            self._settings.store_log_window_size(*self._log_view.GetSize())
            self._settings.store_log_window_position(*self._log_view.GetPosition())
        self._log_view = None
        event.Skip()

    def _on_view_close(self, event):
        if self._log_view is not None:
            self._log_view.Close()
        self._settings.store_main_window_maximized(self._view.IsMaximized())
        if not self._view.IsMaximized():
            self._settings.store_main_window_size(*self._view.GetSize())
            self._settings.store_main_window_position(*self._view.GetPosition())
        event.Skip()

    ###########
    # Private #
    ###########

    def _update_view_from_configuration(self):
        self._view.update_configuration_filename(self._configuration.get_filename(), self._configuration.is_changed())
        self._view.update_configuration_info(self._configuration.get_sample_time(),
                                             self._configuration.get_end_time(),
                                             self._configuration.get_continuous_mode())
        self._view.update_elapsed_time(self._elapsed_time)

    def _show_log(self):
        if self._log_view is None:
            self._log_view = ViewLogger('Log Messages')
            size = self._settings.get_log_window_size()
            if -1 not in size:
                self._log_view.SetSize(size)
            pos = self._settings.get_log_window_position()
            if -1 not in pos:
                self._log_view.SetPosition(pos)
            self._log_view.Maximize(self._settings.get_log_window_maximized())
            self._log_view.Bind(wx.EVT_CLOSE, self._on_close_log)
            self._log_view.show()
        else:
            self._log_view.Raise()

    ##########
    # Public #
    ##########

    def show_view(self):
        self._logger.debug('Show main view')
        self._view.Show()


if __name__ == '__main__':

    from src.models.logger import Logger

    test_logger = Logger(True)
    app = wx.App(redirect=False)
    controller = ControllerMain('ControllerMain Test', test_logger)
    controller.show_view()
    app.MainLoop()
