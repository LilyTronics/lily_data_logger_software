"""
Main controller for the application.
"""

import csv
import os.path

import wx.grid

from src.controllers.controller_check_instruments import ControllerCheckInstruments
from src.controllers.controller_configuration import ControllerConfiguration
from src.controllers.controller_edit_instrument import ControllerEditInstrument
from src.controllers.controller_edit_measurement import ControllerEditMeasurement
from src.models.configuration import Configuration
from src.models.id_manager import IdManager
from src.models.instruments import Instruments
from src.models.measurement_runner import MeasurementRunner
from src.models.settings import Settings
from src.simulators import Simulators
from src.views.view_dialogs import ViewDialogs
from src.views.view_logger import ViewLogger
from src.views.view_main import ViewMain
from src.views.view_progress_dialog import ProgressDialog


class ControllerMain:

    _TIMER_UPDATE_INTERVAL = 250    # ms
    _LED_INTERVAL = 500             # ms

    def __init__(self, view_title, logger):
        self._logger = logger
        self._logger.info("Load main controller")

        self._settings = Settings()
        self._configuration = Configuration()

        self._main_view = self._initialize_main_view(view_title)
        self._log_view = None

        self._logger.info("Show main view")
        self._main_view.Show()

        self._measurement_runner = MeasurementRunner(self._configuration,
                                                     self._measurement_callback)

        self._update_timer = wx.Timer()
        self._update_timer.Bind(wx.EVT_TIMER, self._on_update_timer)
        self._update_timer.Start(self._TIMER_UPDATE_INTERVAL)

        self._led_counter = 0

        wx.CallAfter(self._update_view_from_configuration)
        wx.CallAfter(Simulators.start_simulators, self._logger)

    ###########
    # Private #
    ###########

    def _initialize_main_view(self, view_title):
        frame = ViewMain(view_title, self._on_recent_config_select)
        size = self._settings.get_main_window_size()
        if -1 not in size:
            frame.SetSize(size)
        pos = self._settings.get_main_window_position()
        if -1 not in pos:
            frame.SetPosition(pos)
        frame.Maximize(self._settings.get_main_window_maximized())
        frame.update_recent_configurations(self._settings.get_recent_configurations())
        frame.Bind(wx.EVT_CLOSE, self._on_view_close)
        frame.Bind(wx.EVT_TOOL, self._on_new_configuration,
                   id=IdManager.ID_TOOL_NEW_CONFIGURATION)
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
        frame.Bind(wx.EVT_TOOL, self._on_export_to_csv, id=IdManager.ID_TOOL_EXPORT_CSV)
        frame.Bind(wx.EVT_TOOL, self._on_export_instrument, id=IdManager.ID_TOOL_EXPORT_INSTRUMENT)
        frame.Bind(wx.EVT_TOOL, self._on_show_log, id=IdManager.ID_TOOL_SHOW_LOG)
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

    def _add_config_to_recent_configs(self):
        filename = self._configuration.get_filename()
        if os.path.isfile(filename):
            self._settings.add_to_recent_configurations(filename)
        self._main_view.update_recent_configurations(self._settings.get_recent_configurations())

    def _update_view_from_configuration(self):
        self._main_view.update_configuration_filename(self._configuration.get_filename(),
                                                      self._configuration.is_changed())
        self._main_view.update_configuration_info(self._configuration.get_sample_time(),
                                                  self._configuration.get_end_time(),
                                                  self._configuration.get_continuous_mode())
        self._main_view.update_elapsed_time(0)
        self._main_view.update_led(0)
        self._main_view.update_instruments_list(map(lambda x: x[self._configuration.KEY_NAME],
                                                    self._configuration.get_instruments()))
        self._main_view.update_measurements(map(lambda x: x[self._configuration.KEY_NAME],
                                                self._configuration.get_measurements()))

    def _show_initialize_dialog(self, value):
        ProgressDialog(self._main_view, "Initialize instruments", value)

    def _measurement_callback(self, timestamp, message_type, identifier, value):
        if message_type == self._measurement_runner.MESSAGE_TYPE_STATUS_ERROR:
            if self._main_view.active_dialog is not None:
                wx.CallAfter(self._main_view.active_dialog.destroy)
            wx.CallAfter(ViewDialogs.show_message, self._main_view, identifier, "Process error")
        elif message_type == self._measurement_runner.MESSAGE_TYPE_STATUS_CREATE:
            # Create the instruments
            self._logger.debug("Create instruments")
            wx.CallAfter(self._show_initialize_dialog, value)
        elif message_type == self._measurement_runner.MESSAGE_TYPE_STATUS_INIT:
            # Init the instruments
            self._logger.debug(identifier)
            # Check if dialog is available
            while self._main_view.active_dialog is None:
                wx.MilliSleep(100)
            if self._main_view.active_dialog is not None:
                wx.CallAfter(self._main_view.active_dialog.update, value, identifier)
        elif message_type == self._measurement_runner.MESSAGE_TYPE_STATUS_START:
            # Start the measurements
            self._logger.debug("Start measurements")
            if self._main_view.active_dialog is not None:
                wx.CallAfter(self._main_view.active_dialog.destroy)
        elif message_type == self._measurement_runner.MESSAGE_TYPE_VALUE:
            wx.CallAfter(self._main_view.update_measurement_value, timestamp, identifier, value)
        elif message_type == self._measurement_runner.MESSAGE_TYPE_STATUS_FINISHED:
            # Measurement runner finished
            self._logger.info("Measurements finished")
            wx.CallAfter(self._main_view.update_elapsed_time,
                         int(self._measurement_runner.get_elapsed_time()))
            wx.CallAfter(self._main_view.update_led, 0)
        else:
            self._logger.error("Unknown message type: "
                               f"{timestamp}, {message_type}, {identifier}, {value}")

    ##################
    # Event handlers #
    ##################

    #################
    # Configuration #
    #################

    def _on_new_configuration(self, event):
        btn = ControllerConfiguration.new_config(self._main_view, self._configuration, self._logger)
        if btn != wx.ID_CANCEL:
            self._configuration = Configuration()
        self._update_view_from_configuration()
        event.Skip()

    def _on_open_configuration(self, event):
        ControllerConfiguration.load_from_file(self._main_view, self._configuration, self._logger)
        self._update_view_from_configuration()
        self._add_config_to_recent_configs()
        event.Skip()

    def _on_save_configuration(self, event):
        ControllerConfiguration.save_to_file(self._main_view, self._configuration, self._logger)
        self._update_view_from_configuration()
        self._add_config_to_recent_configs()
        event.Skip()

    def _on_edit_configuration(self, event):
        ControllerConfiguration.edit_configuration(self._main_view, self._configuration,
                                                   self._logger)
        self._update_view_from_configuration()
        event.Skip()

    def _on_recent_config_select(self, event):
        index = event.GetId() - IdManager.ID_RECENT_CONFIG_MENU
        filenames = self._settings.get_recent_configurations()
        if index < len(filenames):
            if os.path.isfile(filenames[index]):
                # Load configuration from file and put it on top of the list
                ControllerConfiguration.load_configuration_from_file(
                    self._main_view, self._configuration, filenames[index], self._logger)
                self._update_view_from_configuration()
                self._add_config_to_recent_configs()
            else:
                ViewDialogs.show_message(self._main_view,
                                         f"The file: '{filenames[index]}' no longer exists. "
                                         "It will be removed from the recent files list.",
                                         "Open configuration")
                self._settings.remove_recent_configuration(filenames[index])
            self._main_view.update_recent_configurations(self._settings.get_recent_configurations())
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
        if (event.GetId() == IdManager.ID_TOOL_START_PROCESS and
                not self._measurement_runner.is_running()):
            self._logger.info("Start measurements")
            dialog_title = "Start process"
            if len(self._configuration.get_measurements()) == 0:
                ViewDialogs.show_message(self._main_view, "Create one or more measurements first.",
                                         dialog_title)
            elif self._measurement_runner.is_running():
                ViewDialogs.show_message(self._main_view, "The process is already running.",
                                         dialog_title)
            else:
                # Make sure we run the latest configuration
                self._update_view_from_configuration()
                self._led_counter = 0
                self._measurement_runner.update_configuration(self._configuration)
                self._measurement_runner.start()
        elif (event.GetId() == IdManager.ID_TOOL_STOP_PROCESS and
              self._measurement_runner.is_running()):
            self._logger.info("Stop measurements")
            self._measurement_runner.stop()

        event.Skip()

    def _on_update_timer(self, event):
        if self._measurement_runner.is_running():
            self._main_view.update_elapsed_time(int(self._measurement_runner.get_elapsed_time()))
            self._led_counter += 1
            if self._led_counter >= self._LED_INTERVAL / self._TIMER_UPDATE_INTERVAL:
                self._main_view.update_led(2)
                self._led_counter = 0
        event.Skip()

    ##########
    # Export #
    ##########

    def _on_export_to_csv(self, event):
        dialog_title = "Export to CSV"
        measurement_data = self._main_view.get_measurement_data()
        if len(measurement_data) <= 1:
            ViewDialogs.show_message(self._main_view, "There is no measurement data.", dialog_title)
        else:
            filename = ViewDialogs.show_save_file(self._main_view, dialog_title, "", "",
                                                  "CSV files (*.csv)|*.csv")
            if filename is not None:
                try:
                    self._logger.debug(f"CSV export to: {filename}")
                    with open(filename, "w", encoding="utf-8", newline="") as fp:
                        writer = csv.writer(fp, quoting=csv.QUOTE_NONNUMERIC)
                        writer.writerow(measurement_data[0])
                        writer.writerows(measurement_data[1:])
                except Exception as e:
                    self._logger.error(str(e))
                    ViewDialogs.show_message(self._main_view,
                                             f"Error when writing file {filename}:\n{e}",
                                             dialog_title)
        event.Skip()

    def _on_export_instrument(self, event):
        dialog_title = "Export instrument"
        name = self._main_view.get_selected_instrument()
        if name == "":
            ViewDialogs.show_message(self._main_view, "Select an instrument first", dialog_title)
        else:
            instrument = Instruments.get_instrument_by_name(
                self._configuration.get_instrument(name)[self._configuration.KEY_SETTINGS]
                [self._configuration.KEY_INSTRUMENT_NAME]
            )
            filename = ViewDialogs.show_save_file(self._main_view, dialog_title, "", "",
                                                  "JSON files (*.json)|*.json")
            if filename is not None:
                try:
                    instrument.export_to_file(filename)
                except Exception as e:
                    self._logger.error(str(e))
                    ViewDialogs.show_message(self._main_view,
                                             f"Error when writing file {filename}:\n{e}",
                                             dialog_title)

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

    from tests.unit_tests.test_gui.test_controller_main import TestControllerMain

    TestControllerMain().run(True)
