"""
Main view for the application
"""

import wx.grid

from src.models.id_manager import IdManager
from src.models.image_data import ImageData
from src.models.time_converter import TimeConverter
from tests.test_environment.test_configurations import TestConfigurations


class ViewMain(wx.Frame):

    _GAP = 5

    _LIST_COL_DATA_SIZE = 120
    _LIST_COL_INDEX_SIZE = 30
    _LIST_COL_NAME_SIZE = 160
    _LIST_COL_STEP_SIZE = 120
    _TABLE_TIME_COL_WIDTH = 110

    _LED_SIZE = (16, 16)
    _COLOR_LED_OFF = "#060"
    _COLOR_LED_ON = "#0f0"

    _MINIMUM_WINDOW_SIZE = (1100, 700)

    def __init__(self, title, select_config_callback, show_test_configurations):
        self.active_dialog = None
        self._select_config_callback = select_config_callback
        self._title = title
        super().__init__(None, wx.ID_ANY, self._title)
        self.SetIcon(wx.Icon(ImageData.app_icon.Bitmap))
        panel = wx.Panel(self)

        lab_box = wx.BoxSizer(wx.HORIZONTAL)
        lab_box.Add(self._create_instruments_controls(panel), 20, wx.EXPAND | wx.ALL, self._GAP)
        lab_box.Add(self._create_measurement_box(panel), 80,
                    wx.EXPAND | wx.TOP | wx.RIGHT | wx.BOTTOM, self._GAP)

        main_box = wx.BoxSizer(wx.VERTICAL)
        main_box.Add(self._create_toolbar(panel, show_test_configurations), 0,
                     wx.EXPAND | wx.ALL, self._GAP)
        main_box.Add(self._create_config_info(panel), 0, wx.EXPAND | wx.ALL, self._GAP)
        main_box.Add(lab_box, 1, wx.EXPAND)

        panel.SetSizer(main_box)

        self.SetInitialSize(self._MINIMUM_WINDOW_SIZE)

    ###########
    # Private #
    ###########

    def _create_toolbar(self, parent, show_test_configurations):
        self._recent_configs = wx.Menu()
        self._recent_configs.Append(1, 'Recent configurations')

        self._toolbar = wx.ToolBar(parent, style=wx.TB_HORIZONTAL | wx.TB_FLAT | wx.TB_NODIVIDER)
        self._toolbar.AddTool(IdManager.ID_TOOL_NEW_CONFIGURATION, "",
                              ImageData.new_config.Bitmap, "New configuration")
        self._toolbar.AddTool(IdManager.ID_TOOL_OPEN_CONFIGURATION, "",
                              ImageData.open_config.Bitmap, "Open configuration",
                              kind=wx.ITEM_DROPDOWN)
        self._toolbar.SetDropdownMenu(IdManager.ID_TOOL_OPEN_CONFIGURATION,
                                      self._recent_configs)
        self._toolbar.AddTool(IdManager.ID_TOOL_SAVE_CONFIGURATION, "",
                              ImageData.save_config.Bitmap, "Save configuration")
        self._toolbar.AddSeparator()
        self._toolbar.AddTool(IdManager.ID_TOOL_EDIT_CONFIGURATION, "",
                              ImageData.settings.Bitmap, "Configuration settings")
        self._toolbar.AddSeparator()
        self._toolbar.AddTool(IdManager.ID_TOOL_CHECK_INSTRUMENTS, "",
                              ImageData.check_instruments.Bitmap, "Check instruments")
        self._toolbar.AddSeparator()
        self._toolbar.AddTool(IdManager.ID_TOOL_START_PROCESS, "",
                              ImageData.start.Bitmap, "Start")
        self._toolbar.AddTool(IdManager.ID_TOOL_STOP_PROCESS, "",
                              ImageData.stop.Bitmap, "Stop")
        self._toolbar.AddSeparator()
        self._toolbar.AddTool(IdManager.ID_TOOL_EXPORT_CSV, "",
                              ImageData.export_csv.Bitmap, "Export measurement data to CSV")
        self._toolbar.AddTool(IdManager.ID_TOOL_EXPORT_INSTRUMENT, "",
                              ImageData.export_instrument.Bitmap, "Export instrument")
        self._toolbar.AddSeparator()
        self._toolbar.AddTool(IdManager.ID_TOOL_SHOW_LOG, "",
                              ImageData.show_log.Bitmap, "Show log")
        if show_test_configurations:
            cmb_config = wx.ComboBox(self._toolbar, IdManager.ID_TOOL_TEST_CONFIG, size=(150, -1))
            cmb_config.SetItems(TestConfigurations.get_configuration_names())
            self._toolbar.AddStretchableSpace()
            self._toolbar.AddControl(cmb_config)
        self._toolbar.Realize()
        return self._toolbar

    def _create_config_info(self, parent):
        box = wx.StaticBoxSizer(wx.StaticBox(parent, wx.ID_ANY, " Configuration: "), wx.HORIZONTAL)

        lbl_sample_time = wx.StaticText(parent, wx.ID_ANY, "Sample time:")
        self._lbl_sample_time = wx.StaticText(parent, IdManager.ID_LABEL_SAMPLE_TIME, "-")
        self._lbl_end_time = wx.StaticText(parent, wx.ID_ANY, "End time:")
        self._value_end_time = wx.StaticText(parent, IdManager.ID_LABEL_END_TIME, "-")
        self._lbl_total_samples = wx.StaticText(parent, wx.ID_ANY, "Total samples:")
        self._value_total_samples = wx.StaticText(parent, IdManager.ID_LABEL_TOTAL_SAMPLES, "-")
        lbl_elapsed_time = wx.StaticText(parent, wx.ID_ANY, "Elapsed time:")
        self._lbl_elapsed_time = wx.StaticText(parent, IdManager.ID_LABEL_ELAPSED_TIME, "-")
        self._activity_led = wx.Panel(parent, wx.ID_ANY, size=self._LED_SIZE,
                                      style=wx.BORDER_SIMPLE)
        self._activity_led.SetBackgroundColour(self._COLOR_LED_OFF)

        box.Add(lbl_sample_time, 0, wx.ALL, self._GAP)
        box.Add(self._lbl_sample_time, 0, wx.ALL, self._GAP)
        box.Add(self._lbl_end_time, 0, wx.ALL, self._GAP)
        box.Add(self._value_end_time, 0, wx.ALL, self._GAP)
        box.Add(self._lbl_total_samples, 0, wx.ALL, self._GAP)
        box.Add(self._value_total_samples, 0, wx.ALL, self._GAP)
        box.Add(lbl_elapsed_time, 0, wx.ALL, self._GAP)
        box.Add(self._lbl_elapsed_time, 0, wx.ALL, self._GAP)
        box.Add(self._activity_led, 0, wx.ALL, self._GAP)

        return box

    def _create_instruments_controls(self, parent):
        box = wx.StaticBoxSizer(wx.StaticBox(parent, wx.ID_ANY, " Instruments: "), wx.VERTICAL)

        self._lst_instruments = wx.ListCtrl(parent, IdManager.ID_LIST_INSTRUMENTS,
                                            style=wx.LC_REPORT | wx.LC_SORT_ASCENDING |
                                            wx.LC_SINGLE_SEL)
        self._lst_instruments.InsertColumn(0, "Name", width=self._LIST_COL_NAME_SIZE)

        btn_add_instrument = wx.Button(parent, IdManager.ID_BTN_ADD_INSTRUMENT, "Add")
        btn_delete_instrument = wx.Button(parent, IdManager.ID_BTN_DELETE_INSTRUMENT, "Delete")

        buttons = wx.BoxSizer(wx.HORIZONTAL)
        buttons.Add(btn_add_instrument, 0)
        buttons.Add(btn_delete_instrument, 0)

        box.Add(self._lst_instruments, 1, wx.EXPAND | wx.ALL, self._GAP)
        box.Add(buttons, 0, wx.ALL, self._GAP)

        return box

    def _create_measurement_box(self, parent):
        box = wx.StaticBoxSizer(wx.StaticBox(parent, wx.ID_ANY, " Measurements: "), wx.VERTICAL)

        grid_panel = wx.Panel(parent, wx.ID_ANY)
        grid_panel.SetBackgroundColour("#abadb3")

        self._grid_measurements = wx.grid.Grid(grid_panel, IdManager.ID_GRID_MEASUREMENTS)
        self._grid_measurements.CreateGrid(0, 1)
        self._grid_measurements.SetColLabelValue(0, "Time")
        self._grid_measurements.SetColSize(0, self._TABLE_TIME_COL_WIDTH)
        self._grid_measurements.EnableEditing(False)
        self._grid_measurements.EnableDragRowSize(False)
        self._grid_measurements.EnableDragColMove(False)
        self._grid_measurements.EnableDragColSize(False)

        btn_add_measurement = wx.Button(parent, IdManager.ID_BTN_ADD_MEASUREMENT, "Add")
        btn_delete_measurement = wx.Button(parent, IdManager.ID_BTN_DELETE_MEASUREMENT, "Delete")

        buttons = wx.BoxSizer(wx.HORIZONTAL)
        buttons.Add(btn_add_measurement, 0)
        buttons.Add(btn_delete_measurement, 0)

        grid_box = wx.BoxSizer(wx.VERTICAL)
        grid_box.Add(self._grid_measurements, 1, wx.EXPAND | wx.ALL, 1)
        grid_panel.SetSizer(grid_box)

        box.Add(grid_panel, 1, wx.EXPAND | wx.ALL, self._GAP)
        box.Add(buttons, 0, wx.ALL, self._GAP)

        return box

    ##########
    # Public #
    ##########

    def get_toolbar(self):
        return self._toolbar

    def update_configuration_filename(self, filename, is_changed):
        title = f"{self._title} - {filename}"
        if is_changed:
            title += " *"
        self.SetTitle(title)

    def update_recent_configurations(self, filenames):
        for item in self._recent_configs.GetMenuItems():
            self._recent_configs.Unbind(wx.EVT_MENU, item, handler=self._select_config_callback)
            self._recent_configs.DestroyItem(item)

        if len(filenames) == 0:
            self._recent_configs.Append(wx.ID_ANY, 'Recent configurations')
        else:
            for i, filename in enumerate(filenames):
                item = self._recent_configs.Append(IdManager.ID_RECENT_CONFIG_MENU + i, filename)
                self._recent_configs.Bind(wx.EVT_MENU, self._select_config_callback, item)

    def update_configuration_info(self, sample_time, end_time, continuous_mode):
        self._lbl_sample_time.SetLabel(TimeConverter.create_duration_time_string(sample_time))
        if continuous_mode:
            self._value_end_time.SetLabel("Continuous mode")
            self._lbl_end_time.Hide()
            self._lbl_total_samples.Hide()
            self._value_total_samples.Hide()
        else:
            self._lbl_end_time.Show()
            self._lbl_total_samples.Show()
            self._value_total_samples.Show()
            self._value_end_time.SetLabel(TimeConverter.create_duration_time_string(end_time))
            total_samples = "-"
            if sample_time > 0 and end_time > 0:
                total_samples = int(end_time / sample_time) + 1
            self._value_total_samples.SetLabel(str(total_samples))

        self._lbl_sample_time.GetParent().Layout()

    def update_elapsed_time(self, elapsed_time):
        self._lbl_elapsed_time.SetLabel(TimeConverter.create_duration_time_string(elapsed_time))
        self._lbl_elapsed_time.GetParent().Layout()

    def update_led(self, mode):
        # Three options:
        # 0: off
        # 1: on
        # 2: invert
        if mode == 0:
            self._activity_led.SetBackgroundColour(self._COLOR_LED_OFF)
        elif mode == 1:
            self._activity_led.SetBackgroundColour(self._COLOR_LED_ON)
        else:
            color = self._activity_led.GetBackgroundColour()
            if color == self._COLOR_LED_OFF:
                self._activity_led.SetBackgroundColour(self._COLOR_LED_ON)
            else:
                self._activity_led.SetBackgroundColour(self._COLOR_LED_OFF)
        self._activity_led.Refresh()

    def update_instruments_list(self, instrument_names):
        self._lst_instruments.DeleteAllItems()
        for name in instrument_names:
            item = wx.ListItem()
            item.SetId(self._lst_instruments.GetItemCount())
            item.SetText(name)
            self._lst_instruments.InsertItem(item)
        self._lst_instruments.SetColumnWidth(0, wx.LIST_AUTOSIZE)
        if self._lst_instruments.GetColumnWidth(0) < self._LIST_COL_NAME_SIZE:
            self._lst_instruments.SetColumnWidth(0, self._LIST_COL_NAME_SIZE)

    def get_selected_instrument(self):
        item_text = ""
        index = self._lst_instruments.GetFirstSelected()
        if index >= 0:
            item_text = self._lst_instruments.GetItemText(index, 0)
        return item_text

    def update_measurements(self, measurement_names):
        if self._grid_measurements.GetNumberCols() > 1:
            self._grid_measurements.DeleteCols(1, self._grid_measurements.GetNumberCols() - 1)
        if self._grid_measurements.GetNumberRows() > 0:
            self._grid_measurements.DeleteRows(0, self._grid_measurements.GetNumberRows())
        for i, name in enumerate(measurement_names):
            self._grid_measurements.AppendCols(1)
            self._grid_measurements.SetColLabelValue(i + 1, name)
            self._grid_measurements.AutoSizeColLabelSize(i + 1)
            size = self._grid_measurements.GetColSize(i + 1) + self._GAP
            self._grid_measurements.SetColSize(i + 1, size)
            self._grid_measurements.SetColMinimalWidth(i + 1, size)
        self._grid_measurements.AppendRows(1)

    def get_selected_measurement(self):
        cols = self._grid_measurements.GetSelectedCols()
        if len(cols) == 1 and cols[0] > 0:
            return self._grid_measurements.GetColLabelValue(cols[0])
        return None

    def update_measurement_value(self, timestamp, measurement, value):
        timestamp = TimeConverter.get_timestamp(timestamp)
        col = -1
        for i in range(self._grid_measurements.GetNumberCols()):
            if self._grid_measurements.GetColLabelValue(i) == measurement:
                col = i
                break
        if col > 0:
            row = -1
            # Check from bottom to top (faster)
            for i in range(self._grid_measurements.GetNumberRows() - 1, -1, -1):
                if self._grid_measurements.GetCellValue(i, 0) == timestamp:
                    row = i
                    break
            if row < 0:
                # Timestamp not found, add it
                row = self._grid_measurements.GetNumberRows() - 1
                self._grid_measurements.SetCellValue(row, 0, timestamp)
                self._grid_measurements.SetCellAlignment(row, 0, wx.ALIGN_CENTER, wx.ALIGN_CENTER)
                self._grid_measurements.AppendRows(1)
            # Add measured value
            self._grid_measurements.SetCellValue(row, col, str(value))
            self._grid_measurements.SetCellAlignment(row, col, wx.ALIGN_CENTER, wx.ALIGN_CENTER)
            self._grid_measurements.AutoSizeColumn(col)
            size = self._grid_measurements.GetColSize(col) + self._GAP
            self._grid_measurements.SetColSize(col, size)
            self._grid_measurements.MakeCellVisible(row + 1, 0)

    def get_measurement_data(self):
        data = []
        if self._grid_measurements.GetNumberRows() > 0:
            row_data = []
            for col in range(self._grid_measurements.GetNumberCols()):
                row_data.append(self._grid_measurements.GetColLabelValue(col))
            data.append(row_data)
            for row in range(self._grid_measurements.GetNumberRows()):
                row_data = []
                # Only add row if it has a timestamp
                if self._grid_measurements.GetCellValue(row, 0) != "":
                    for col in range(self._grid_measurements.GetNumberCols()):
                        value = self._grid_measurements.GetCellValue(row, col)
                        try:
                            value = float(value)
                        except (Exception,):
                            pass
                        row_data.append(value)
                    data.append(row_data)

        return data


if __name__ == "__main__":

    from tests.unit_tests.test_gui.test_controller_main import TestControllerMain

    TestControllerMain().run(True)
