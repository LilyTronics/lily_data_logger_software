"""
Main controller for the application.
"""

import wx

from src.models.configuration import Configuration
from src.models.settings import Settings
from src.views.view_dialogs import show_confirm
from src.views.view_dialogs import show_message
from src.views.view_dialogs import show_open_file
from src.views.view_dialogs import show_save_file
from src.views.view_edit_configuration import ViewEditConfiguration
from src.views.view_logger import ViewLogger
from src.views.view_main import ViewMain


class ControllerMain(object):

    def __init__(self, view_title, logger):
        self._logger = logger
        self._logger.info('Load main controller')
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
        self._view.Bind(wx.EVT_TOOL, self._on_open_configuration, id=self._view.ID_TOOL_OPEN_CONFIGURATION)
        self._view.Bind(wx.EVT_TOOL, self._on_save_configuration, id=self._view.ID_TOOL_SAVE_CONFIGURATION)
        self._view.Bind(wx.EVT_TOOL, self._on_edit_configuration, id=self._view.ID_TOOL_EDIT_CONFIGURATION)
        self._view.Bind(wx.EVT_TOOL, self._on_show_log, id=self._view.ID_TOOL_SHOW_LOG)
        self._configuration = Configuration()
        self._elapsed_time = 0
        self._log_view = None
        self._logger.info('Show main view')
        self._view.Show()

        wx.CallAfter(self._update_view_from_configuration)

    ##################
    # Event handlers #
    ##################

    def _on_open_configuration(self, event):
        self._check_configuration_is_changed()
        filename = show_open_file(self._view, 'Open configuration', file_filter='Configuration files (*.json)|*.json')
        if filename is not None:
            self._logger.debug("Load configuration from file: '%s'" % filename)
            try:
                self._configuration.load_from_file(filename)
                self._update_view_from_configuration()
            except Exception as e:
                self._logger.error(str(e))
                show_message(self._view, "Error when reading file '%s':\n'%s'" % (filename, e),
                             'Open configuration')

        event.Skip()

    def _on_save_configuration(self, event):
        self._save_configuration()
        event.Skip()

    def _on_edit_configuration(self, event):
        dlg = ViewEditConfiguration(self._view)
        dlg.set_sample_time(self._configuration.get_sample_time())
        dlg.set_end_time(self._configuration.get_end_time())
        dlg.set_continuous_mode(self._configuration.get_continuous_mode())
        if dlg.ShowModal() == wx.ID_OK:
            self._logger.info('Edit configuration settings')
            current_sample_time = self._configuration.get_sample_time()
            new_sample_time = dlg.get_sample_time()
            current_end_time = self._configuration.get_end_time()
            new_end_time = dlg.get_end_time()
            current_continuous_mode = self._configuration.get_continuous_mode()
            new_continuous_mode = dlg.get_continuous_mode()
            self._configuration.set_sample_time(new_sample_time)
            self._configuration.set_end_time(new_end_time)
            self._configuration.set_continuous_mode(new_continuous_mode)
            if current_sample_time != new_sample_time:
                self._logger.debug('Sample time changed from {} to {} seconds'.format(current_sample_time,
                                                                                      new_sample_time))
            if current_end_time != new_end_time:
                self._logger.debug('End time changed from {} to {} seconds'.format(current_end_time,
                                                                                   new_end_time))
            if current_continuous_mode != new_continuous_mode:
                self._logger.debug('Continuous mode changed from {} to {}'.format(current_continuous_mode,
                                                                                  new_continuous_mode))
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
        self._check_configuration_is_changed()
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

    def _check_configuration_is_changed(self):
        if self._configuration.is_changed():
            if show_confirm(self._view, 'The configuration is changed. Save configuration?', 'Save configuration') == \
                    wx.ID_YES:
                self._save_configuration()

    def _save_configuration(self):
        filename = show_save_file(self._view, 'Save configuration', file_filter='Configuration files (*.json)|*.json')
        if filename is not None:
            self._logger.debug("Save configuration to file: '%s'" % filename)
            try:
                self._configuration.save_to_file(filename)
                self._update_view_from_configuration()
            except Exception as e:
                self._logger.error(str(e))
                show_message(self._view, "Error when writing file '%s':\n'%s'" % (filename, e),
                             'Save configuration')

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


if __name__ == '__main__':

    from src.models.logger import Logger

    test_logger = Logger(True)
    app = wx.App(redirect=False)
    controller = ControllerMain('ControllerMain Test', test_logger)
    app.MainLoop()
