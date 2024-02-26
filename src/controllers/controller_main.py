"""
Main controller for the application.
"""

import wx.grid

from src.controllers.controller_check_instruments import ControllerCheckInstruments
from src.controllers.controller_configuration import ControllerConfiguration
from src.controllers.controller_edit_instrument import ControllerEditInstrument
from src.controllers.controller_edit_measurement import ControllerEditMeasurement
from src.models.configuration import Configuration
from src.models.id_manager import IdManager
from src.models.measurement_runner import MeasurementRunner
from src.models.settings import Settings
from src.views.view_dialogs import ViewDialogs
from src.views.view_logger import ViewLogger
from src.views.view_main import ViewMain
from src.simulators import Simulators
from tests.test_environment.test_configurations import TestConfigurations


class ControllerMain:

    def __init__(self, view_title, logger, show_test_configurations=False):
        self._logger = logger
        self._logger.info("Load main controller")

        self._settings = Settings()
        self._configuration = Configuration()
        self._elapsed_time = 0

        self._main_view = self._initialize_main_view(view_title, show_test_configurations)
        self._log_view = None

        self._logger.info("Show main view")
        self._main_view.Show()

        self._measurement_runner = MeasurementRunner(self._configuration,
                                                     self._measurement_callback)

        wx.CallAfter(self._update_view_from_configuration)
        wx.CallAfter(Simulators.start_simulators, self._logger)

    ###########
    # Private #
    ###########

    def _initialize_main_view(self, view_title, show_test_configurations):
        frame = ViewMain(view_title, show_test_configurations)
        size = self._settings.get_main_window_size()
        if -1 not in size:
            frame.SetSize(size)
        pos = self._settings.get_main_window_position()
        if -1 not in pos:
            frame.SetPosition(pos)
        frame.Maximize(self._settings.get_main_window_maximized())
        frame.Bind(wx.EVT_CLOSE, self._on_view_close)
        frame.Bind(wx.EVT_TOOL, self._on_open_configuration,
                   id=IdManager.ID_TOOL_OPEN_CONFIGURATION)
        frame.Bind(wx.EVT_TOOL, self._on_save_configuration,
                   id=IdManager.ID_TOOL_SAVE_CONFIGURATION)
        frame.Bind(wx.EVT_TOOL, self._on_edit_configuration,
                   id=IdManager.ID_TOOL_EDIT_CONFIGURATION)
        frame.Bind(wx.EVT_TOOL, self._on_check_instruments,
                   id=IdManager.ID_TOOL_CHECK_INSTRUMENTS)
        frame.Bind(wx.EVT_TOOL, self._on_start_stop_process, id=IdManager.ID_TOOL_START_PROCESS)
        frame.Bind(wx.EVT_TOOL, self._on_start_stop_process, id=IdManager.ID_TOOL_STOP_PROCESS)
        frame.Bind(wx.EVT_TOOL, self._on_show_log, id=IdManager.ID_TOOL_SHOW_LOG)
        frame.Bind(wx.EVT_COMBOBOX, self._on_test_config, id=IdManager.ID_TOOL_TEST_CONFIG)
        frame.Bind(wx.EVT_BUTTON, self._on_edit_instrument, id=IdManager.ID_BTN_ADD_INSTRUMENT)
        frame.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self._on_edit_instrument,
                   id=IdManager.ID_LIST_INSTRUMENTS)
        frame.Bind(wx.EVT_BUTTON, self._on_delete_instrument, id=IdManager.ID_BTN_DELETE_INSTRUMENT)
        frame.Bind(wx.EVT_BUTTON, self._on_edit_measurement, id=IdManager.ID_BTN_ADD_MEASUREMENT)
        frame.Bind(wx.grid.EVT_GRID_LABEL_LEFT_DCLICK, self._on_edit_measurement,
                   id=IdManager.ID_GRID_MEASUREMENTS)
        frame.Bind(wx.EVT_BUTTON, self._on_delete_measurement,
                   id=IdManager.ID_BTN_DELETE_MEASUREMENT)

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
        self._main_view.update_measurements(map(lambda x: x[self._configuration.KEY_NAME],
                                                self._configuration.get_measurements()))

    def _measurement_callback(self, timestamp, message_type, identifier, value):
        print(timestamp, message_type, identifier, value)
        if message_type == self._measurement_runner.MESSAGE_TYPE_VALUE:
            self._main_view.update_measurement_value(timestamp, identifier, value)


    ##################
    # Event handlers #
    ##################

    #################
    # Configuration #
    #################

    def _on_open_configuration(self, event):
        ControllerConfiguration.load_from_file(self._main_view, self._configuration, self._logger)
        self._update_view_from_configuration()
        event.Skip()

    def _on_save_configuration(self, event):
        ControllerConfiguration.save_to_file(self._main_view, self._configuration, self._logger)
        self._update_view_from_configuration()
        event.Skip()

    def _on_edit_configuration(self, event):
        ControllerConfiguration.edit_configuration(self._main_view, self._configuration,
                                                   self._logger)
        self._update_view_from_configuration()
        event.Skip()

    def _on_test_config(self, event):
        self._configuration = TestConfigurations.get_configuration(event.GetString())
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

    def _on_check_instruments(self, event):
        ControllerCheckInstruments(self._main_view, self._configuration)
        event.Skip()

    ################
    # Measurements #
    ################

    def _on_edit_measurement(self, event):
        name = None
        if event.GetId() == IdManager.ID_BTN_ADD_MEASUREMENT:
            name = ""
        if event.GetId() == IdManager.ID_GRID_MEASUREMENTS:
            name = self._main_view.get_selected_measurement()
        if name is not None:
            ControllerEditMeasurement.edit_measurement(self._main_view, self._configuration, name)
            self._update_view_from_configuration()
        event.Skip()

    def _on_delete_measurement(self, event):
        ControllerEditMeasurement.delete_measurement(self._main_view, self._configuration)
        self._update_view_from_configuration()
        event.Skip()

    ###########
    # Process #
    ###########

    def _on_start_stop_process(self, event):
        if event.GetId() == IdManager.ID_TOOL_START_PROCESS:
            dialog_title = "Start Process"
            if len(self._configuration.get_measurements()) == 0:
                ViewDialogs.show_message(self._main_view, "Create one or more measurements first.",
                                         dialog_title)
            elif self._measurement_runner.is_running():
                ViewDialogs.show_message(self._main_view, "The process is already running.",
                                         dialog_title)
            else:
                # Make sure we run the latest configuration
                self._measurement_runner.update_configuration(self._configuration)
                self._measurement_runner.start()
        elif event.GetId() == IdManager.ID_TOOL_STOP_PROCESS:
            self._measurement_runner.stop()

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

    #############
    # View main #
    #############

    def _on_view_close(self, event):
        Simulators.stop_simulators(self._logger)
        ControllerConfiguration.check_configuration_is_changed(self._main_view, self._configuration,
                                                               self._logger)
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

    import pylint
    from tests.unit_tests.test_gui.test_controller_main import TestControllerMain

    TestControllerMain().run(True)
    pylint.run_pylint([__file__])
