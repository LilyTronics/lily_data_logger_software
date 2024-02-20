"""
Main view for the application
"""

import wx.grid

from src.models.id_manager import IdManager
from src.models.image_data import ImageData
from src.models.time_converter import TimeConverter


# pylint: disable=too-many-instance-attributes
class ViewMain(wx.Frame):

    _GAP = 5

    _LIST_COL_DATA_SIZE = 120
    _LIST_COL_INDEX_SIZE = 30
    _LIST_COL_NAME_SIZE = 160
    _LIST_COL_STEP_SIZE = 120
    _TABLE_MIN_COL_WIDTH = 100

    _LED_SIZE = (16, 16)
    _COLOR_LED_OFF = "#060"

    _MINIMUM_WINDOW_SIZE = (1100, 700)

    def __init__(self, title):
        self.active_dialog = None
        self._title = title
        super().__init__(None, wx.ID_ANY, self._title)
        panel = wx.Panel(self)

        lab_box = wx.BoxSizer(wx.HORIZONTAL)
        lab_box.Add(self._create_instruments_controls(panel), 20, wx.EXPAND | wx.ALL, self._GAP)
        lab_box.Add(self._create_measurement_box(panel), 80,
                    wx.EXPAND | wx.TOP | wx.RIGHT | wx.BOTTOM, self._GAP)

        main_box = wx.BoxSizer(wx.VERTICAL)
        main_box.Add(self._create_toolbar(panel), 0, wx.EXPAND | wx.ALL, self._GAP)
        main_box.Add(self._create_config_info(panel), 0, wx.EXPAND | wx.ALL, self._GAP)
        main_box.Add(lab_box, 1, wx.EXPAND)

        panel.SetSizer(main_box)

        self.SetInitialSize(self._MINIMUM_WINDOW_SIZE)

    ###########
    # Private #
    ###########

    def _create_toolbar(self, parent):
        tools = [
            (IdManager.ID_TOOL_OPEN_CONFIGURATION, ImageData.open_config.Bitmap,
             "Open configuration"),
            (IdManager.ID_TOOL_SAVE_CONFIGURATION, ImageData.save_config.Bitmap,
             "Save configuration"),
            (0,),
            (IdManager.ID_TOOL_EDIT_CONFIGURATION, ImageData.settings.Bitmap,
             "Configuration settings"),
            (0,),
            (IdManager.ID_TOOL_CHECK_INSTRUMENTS, ImageData.check_instruments.Bitmap,
             "Check instruments"),
            (0,),
            (IdManager.ID_TOOL_START_PROCESS, ImageData.start.Bitmap, "Start"),
            (IdManager.ID_TOOL_STOP_PROCESS, ImageData.stop.Bitmap, "Stop"),
            (0,),
            (IdManager.ID_TOOL_EXPORT_CSV, ImageData.export_csv.Bitmap,
             "Export measurement data to CSV"),
            (IdManager.ID_TOOL_EXPORT_INSTRUMENT, ImageData.export_instrument.Bitmap,
             "Export instrument"),
            (0,),
            (IdManager.ID_TOOL_SHOW_LOG, ImageData.show_log.Bitmap, "Show log"),
        ]
        self._toolbar = wx.ToolBar(parent, style=wx.TB_HORIZONTAL | wx.TB_FLAT | wx.TB_NODIVIDER)
        for tool in tools:
            if tool[0] == 0:
                self._toolbar.AddSeparator()
            else:
                self._toolbar.AddTool(tool[0], "", tool[1], tool[2])
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
        self._grid_measurements.SetColMinimalWidth(0, self._TABLE_MIN_COL_WIDTH)
        self._grid_measurements.AutoSizeColLabelSize(0)
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
        self._grid_measurements.AppendRows(1)

    def get_selected_measurement(self):
        cols = self._grid_measurements.GetSelectedCols()
        if len(cols) == 1 and cols[0] > 0:
            return self._grid_measurements.GetColLabelValue(cols[0])
        return None


if __name__ == "__main__":

    import pylint
    from tests.unit_tests.test_gui.test_controller_main import TestControllerMain

    TestControllerMain().run(True)
    pylint.run_pylint([__file__])
