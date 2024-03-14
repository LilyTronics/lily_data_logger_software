"""
View for editing a measurement.
"""

import wx

from src.models.id_manager import IdManager
from src.views.view_dialogs import ViewDialogs


class ViewEditMeasurement(wx.Dialog):

    _GAP = 5

    def __init__(self, parent, title, configuration, name):
        super().__init__(parent, wx.ID_ANY, title)
        self.active_dialog = None
        self._config = configuration
        self._old_name = name

        box = wx.BoxSizer(wx.VERTICAL)
        box.Add(self._create_controls(), 0, wx.EXPAND | wx.ALL, self._GAP)
        box.Add(self._create_buttons_box(), 0, wx.ALIGN_RIGHT | wx.ALL, self._GAP)

        self.SetSizer(box)
        self.SetInitialSize((400, -1))
        self.CenterOnParent()

        self.Bind(wx.EVT_BUTTON, self._on_ok_click, id=wx.ID_OK)

    def _create_controls(self):
        lbl_name = wx.StaticText(self, wx.ID_ANY, "Name:")
        self._txt_name = wx.TextCtrl(self, IdManager.ID_MEASUREMENT_NAME)
        lbl_instrument = wx.StaticText(self, wx.ID_ANY, "Instrument:")
        self._cmb_instrument = wx.ComboBox(self, IdManager.ID_CMB_MEASUREMENT_INSTRUMENT,
                                           style=wx.CB_READONLY)
        lbl_measurement = wx.StaticText(self, wx.ID_ANY, "Measurement:")
        self._cmb_measurement = wx.ComboBox(self, IdManager.ID_CMB_MEASUREMENT,
                                            style=wx.CB_READONLY)
        lbl_gain = wx.StaticText(self, wx.ID_ANY, "Gain:")
        self._txt_gain = wx.TextCtrl(self, IdManager.ID_GAIN, size=(80, -1))
        lbl_offset = wx.StaticText(self, wx.ID_ANY, "Offset:")
        self._txt_offset = wx.TextCtrl(self, IdManager.ID_OFFSET, size=(80, -1))
        lbl_info = wx.StaticText(self, wx.ID_ANY,
                                 "measurement value = value from instrument * gain + offset")

        grid = wx.GridBagSizer(self._GAP, self._GAP)
        grid.Add(lbl_name, (0, 0), wx.DefaultSpan, wx.ALIGN_CENTER_VERTICAL)
        grid.Add(self._txt_name, (0, 1), wx.DefaultSpan, wx.ALIGN_CENTER_VERTICAL)
        grid.Add(lbl_instrument, (1, 0), wx.DefaultSpan, wx.ALIGN_CENTER_VERTICAL)
        grid.Add(self._cmb_instrument, (1, 1), wx.DefaultSpan, wx.ALIGN_CENTER_VERTICAL)
        grid.Add(lbl_measurement, (2, 0), wx.DefaultSpan, wx.ALIGN_CENTER_VERTICAL)
        grid.Add(self._cmb_measurement, (2, 1), wx.DefaultSpan, wx.ALIGN_CENTER_VERTICAL)
        grid.Add(lbl_gain, (3, 0), wx.DefaultSpan, wx.ALIGN_CENTER_VERTICAL)
        grid.Add(self._txt_gain, (3, 1), wx.DefaultSpan, wx.ALIGN_CENTER_VERTICAL)
        grid.Add(lbl_offset, (4, 0), wx.DefaultSpan, wx.ALIGN_CENTER_VERTICAL)
        grid.Add(self._txt_offset, (4, 1), wx.DefaultSpan, wx.ALIGN_CENTER_VERTICAL)
        grid.Add(lbl_info, (5, 0), (1, 2), wx.ALIGN_CENTER_VERTICAL)

        box = wx.BoxSizer(wx.VERTICAL)
        box.Add(grid, 0, wx.EXPAND | wx.ALL, self._GAP)

        return box

    def _create_buttons_box(self):
        btn_ok = wx.Button(self, wx.ID_OK, "Ok")
        btn_cancel = wx.Button(self, wx.ID_CANCEL, "Cancel")

        box = wx.BoxSizer(wx.HORIZONTAL)
        box.Add(btn_ok, 0, wx.ALL, self._GAP)
        box.Add(btn_cancel, 0, wx.ALL, self._GAP)

        return box

    ##################
    # Event handlers #
    ##################

    def _on_ok_click(self, event):
        name = self._txt_name.GetValue().strip()
        if name == "":
            ViewDialogs.show_message(self, "Enter a name.", "Edit measurement")
            return
        if self._old_name != name:
            measurement = self._config.get_measurement(name)
            if measurement is not None:
                ViewDialogs.show_message(self, "A measurement with the name '{name}' already exist",
                                         self.GetTitle())
                return

        if self._cmb_instrument.GetValue() == "":
            ViewDialogs.show_message(self, "Select an instrument.", "Edit measurement")
            return

        if self._cmb_measurement.GetValue() == "":
            ViewDialogs.show_message(self, "Select a measurement.", "Edit measurement")
            return

        value = ""
        try:
            value = "gain"
            float(self._txt_gain.GetValue().strip())
            value = "offset"
            float(self._txt_offset.GetValue().strip())
        except ValueError:
            ViewDialogs.show_message(self, f"Enter a numeric value for the {value}.",
                                     "Edit measurement")
            return

        event.Skip()

    ##########
    # Public #
    ##########

    def get_name(self):
        return self._txt_name.GetValue().strip()

    def set_name(self, value):
        self._txt_name.SetValue(value)

    def get_instrument(self):
        return self._cmb_instrument.GetValue()

    def set_list_of_instruments(self, instruments):
        self._cmb_instrument.SetItems(instruments)
        self._cmb_instrument.GetParent().Layout()

    def set_instrument(self, value):
        self._cmb_instrument.SetValue(value)

    def get_measurement(self):
        return self._cmb_measurement.GetValue()

    def set_list_of_measurements(self, measurements):
        self._cmb_measurement.SetItems(measurements)
        self._cmb_measurement.GetParent().Layout()

    def set_measurement(self, value):
        self._cmb_measurement.SetValue(value)

    def get_gain(self):
        return float(self._txt_gain.GetValue().strip())

    def set_gain(self, value):
        self._txt_gain.SetValue(str(value))

    def get_offset(self):
        return float(self._txt_offset.GetValue().strip())

    def set_offset(self, value):
        self._txt_offset.SetValue(str(value))


if __name__ == "__main__":

    from tests.unit_tests.test_gui.test_controller_edit_measurement import (
        TestControllerEditInstrument)

    TestControllerEditInstrument().run(True)
