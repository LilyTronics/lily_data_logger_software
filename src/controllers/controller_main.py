"""
Main controller for the application.
"""

import wx

from src.controllers.controller_configuration import ControllerConfiguration
from src.controllers.controller_edit_instrument import ControllerEditInstrument
from src.models.configuration import Configuration
from src.models.id_manager import IdManager
from src.models.settings import Settings
from src.views.view_logger import ViewLogger
from src.views.view_main import ViewMain
from src.simulators import start_simulators
from src.simulators import stop_simulators


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
        wx.CallAfter(start_simulators, self._logger)

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
        frame.Bind(wx.EVT_BUTTON, self._on_edit_instrument, id=IdManager.ID_BTN_ADD_INSTRUMENT)
        frame.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self._on_edit_instrument, id=IdManager.ID_LIST_INSTRUMENTS)
        frame.Bind(wx.EVT_BUTTON, self._on_delete_instrument, id=IdManager.ID_BTN_DELETE_INSTRUMENT)
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
        self._main_view.update_instruments_list(map(lambda x: x[self._configuration.KEY_NAME],
                                                    self._configuration.get_instruments()))

    ##################
    # Event handlers #
    ##################

    #################
    # Configuration #
    #################

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

    ##############
    # Instrument #
    ##############

    def _on_edit_instrument(self, event):
        name = ""
        if event.GetId() == IdManager.ID_LIST_INSTRUMENTS:
            name = event.GetText()
        ControllerEditInstrument.edit_instrument(self._main_view, self._configuration, name)
        self._update_view_from_configuration()
        event.Skip()

    def _on_delete_instrument(self, event):
        ControllerEditInstrument.delete_instrument(self._main_view, self._configuration)
        self._update_view_from_configuration()
        event.Skip()

    ##############
    # Log viewer #
    ##############

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

    # View main

    def _on_view_close(self, event):
        stop_simulators(self._logger)
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


if __name__ == "__main__":

    from tests.unit_tests.test_controller_main import TestControllerMain

    TestControllerMain().run()
