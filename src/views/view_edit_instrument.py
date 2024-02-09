"""
Edit instrument view.
"""

import wx

from src.models.id_manager import IdManager
from src.views.view_dialogs import show_message


class ViewEditInstrument(wx.Dialog):

    _GAP = 5
    _WINDOW_SIZE = (500, -1)
    _CONSOLE_SIZE = (-1, 150)

    def __init__(self, parent, title, configuration, old_name):
        super(ViewEditInstrument, self).__init__(parent, wx.ID_ANY, title)
        self.active_dialog = None
        self._config = configuration
        self._old_name = old_name
        self._settings_controls = {}
        box = wx.BoxSizer(wx.VERTICAL)
        box.Add(self._create_main_settings_box(), 0, wx.EXPAND | wx.ALL, self._GAP)
        box.Add(self._create_instrument_settings_box(), 0, wx.EXPAND | wx.ALL, self._GAP)
        box.Add(self._create_test_box(), 0, wx.EXPAND | wx.ALL, self._GAP)
        box.Add(self._create_buttons_box(), 0, wx.ALIGN_RIGHT | wx.ALL, self._GAP)
        self.Bind(wx.EVT_BUTTON, self._on_ok_click, id=wx.ID_OK)
        self.SetSizer(box)
        self.SetInitialSize(self._WINDOW_SIZE)
        self.CenterOnParent()

    ###########
    # Private #
    ###########

    def _create_main_settings_box(self):
        box = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, " Settings: "), wx.VERTICAL)
        lbl_name = wx.StaticText(self, wx.ID_ANY, "Name:")
        self._txt_name = wx.TextCtrl(self, IdManager.ID_INSTRUMENT_NAME)
        lbl_instrument = wx.StaticText(self, wx.ID_ANY, "Instrument:")
        self._cmb_instrument = wx.ComboBox(self, IdManager.ID_CMB_INSTRUMENT, style=wx.CB_READONLY)
        self._lbl_info = wx.StaticText(self, wx.ID_ANY, "")
        self._lbl_info.Hide()
        grid = wx.GridBagSizer(self._GAP, self._GAP)
        grid.Add(lbl_name, (0, 0), wx.DefaultSpan, wx.ALIGN_CENTER_VERTICAL)
        grid.Add(self._txt_name, (0, 1), wx.DefaultSpan, wx.ALIGN_CENTER_VERTICAL | wx.EXPAND)
        grid.Add(lbl_instrument, (1, 0), wx.DefaultSpan, wx.ALIGN_CENTER_VERTICAL)
        grid.Add(self._cmb_instrument, (1, 1), wx.DefaultSpan, wx.ALIGN_CENTER_VERTICAL)
        grid.Add(self._lbl_info, (2, 1), wx.DefaultSpan, wx.ALIGN_CENTER_VERTICAL)
        grid.AddGrowableCol(1)
        box.Add(grid, 0, wx.EXPAND | wx.ALL, self._GAP)
        return box

    def _create_instrument_settings_box(self):
        self._lbl_no_settings = wx.StaticText(self, wx.ID_ANY, "No settings")
        self._settings_grid = wx.GridBagSizer(self._GAP, self._GAP)
        box = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, " Instrument settings: "), wx.VERTICAL)
        box.Add(self._lbl_no_settings, 0, wx.EXPAND | wx.ALL, self._GAP)
        box.Add(self._settings_grid, 0, wx.EXPAND | wx.ALL, self._GAP)
        return box

    def _create_test_box(self):
        self._txt_console = wx.TextCtrl(self, IdManager.ID_TEST_CONSOLE, size=self._CONSOLE_SIZE,
                                        style=wx.TE_MULTILINE | wx.TE_DONTWRAP | wx.TE_READONLY | wx.TE_RICH)
        self._txt_console.SetFont(wx.Font(9, wx.FONTFAMILY_TELETYPE, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False))
        btn_test = wx.Button(self, IdManager.ID_BTN_SETTINGS_TEST, "Test Settings")
        box = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, " Test settings: "), wx.VERTICAL)
        box.Add(self._txt_console, 0, wx.EXPAND | wx.ALL, self._GAP)
        box.Add(btn_test, 0, wx.ALIGN_LEFT | wx.ALL, self._GAP)
        return box

    def _create_buttons_box(self):
        btn_ok = wx.Button(self, wx.ID_OK, "OK")
        btn_cancel = wx.Button(self, wx.ID_CANCEL, "Cancel")
        box = wx.BoxSizer(wx.HORIZONTAL)
        box.Add(btn_ok, 0, wx.ALL, self._GAP)
        box.Add(btn_cancel, 0, wx.ALL, self._GAP)
        return box

    def _process_callables(self, callables):
        progress = wx.ProgressDialog("Update controls", "", maximum=len(callables), parent=self,
                                     style=wx.PD_APP_MODAL | wx.PD_AUTO_HIDE)
        i = 0
        for label, ctrl, function, default in callables:
            progress.Update(i, "Update {}".format(label.lower()))
            progress.Fit()
            ctrl.SetItems(function())
            ctrl.SetValue(default)
            i += 1
        progress.Destroy()
        self.Raise()

    ##################
    # Event handlers #
    ##################

    def _on_ok_click(self, event):
        name = self._txt_name.GetValue().strip()
        if name == "":
            show_message(self, "Enter a name", self.GetTitle())
            return
        if self._old_name != name:
            instrument = self._config.get_instrument(name)
            if instrument is not None:
                show_message(self, "An instrument with the name '{}' already exist".format(name), self.GetTitle())
                return
        instrument = self._cmb_instrument.GetValue()
        if instrument == "":
            show_message(self, "Select an instrument", self.GetTitle())
            return
        for parameter_name in self._settings_controls.keys():
            if self._settings_controls[parameter_name].GetValue().strip() == "":
                show_message(self, "One of the settings has no value.", self.GetTitle())
                return

        event.Skip()

    ##########
    # Public #
    ##########

    def get_settings_controls(self):
        return self._settings_controls

    def set_name(self, name):
        self._txt_name.SetValue(name)

    def get_name(self):
        return self._txt_name.GetValue().strip()

    def set_instrument_names(self, instrument_names):
        instrument_names.insert(0, "")
        self._cmb_instrument.SetItems(instrument_names)
        self._cmb_instrument.GetParent().Layout()

    def set_instrument_name(self, name):
        self._cmb_instrument.SetValue("")
        if name in self._cmb_instrument.GetItems():
            self._cmb_instrument.SetValue(name)

    def set_instrument_info(self, info):
        if info == "":
            self._lbl_info.Hide()
        else:
            self._lbl_info.Show()
            self._lbl_info.SetLabel(info)
        self._lbl_info.GetParent().Layout()

    def get_selected_instrument_name(self):
        return self._cmb_instrument.GetValue()

    def update_instrument_settings_controls(self, settings_controls):
        self.clear_console()
        self._settings_grid.Clear(True)
        self._lbl_no_settings.Show()
        self._settings_controls = {}
        callables = []
        if len(settings_controls.keys()) > 0:
            self._lbl_no_settings.Hide()
            row = 0
            for key in settings_controls.keys():
                control = settings_controls[key]
                lbl = wx.StaticText(self, wx.ID_ANY, "{}:".format(control["label"]))
                if control["control"] is wx.ComboBox:
                    ctrl = control["control"](self, wx.ID_ANY, style=wx.CB_READONLY)
                    data = control["data"]
                    if callable(data):
                        callables.append((control["label"], ctrl, data, control["default"]))
                    else:
                        ctrl.SetItems(data)
                    ctrl.SetValue(control["default"])
                elif control["control"] is wx.TextCtrl:
                    ctrl = control["control"](self, wx.ID_ANY, control["default"])
                else:
                    raise Exception("Control '{}' is not supported".format(control["control"]))
                self._settings_controls[key] = ctrl
                self._settings_grid.Add(lbl, (row, 0), wx.DefaultSpan, wx.ALIGN_CENTER_VERTICAL)
                self._settings_grid.Add(ctrl, (row, 1), wx.DefaultSpan, wx.ALIGN_CENTER_VERTICAL | wx.EXPAND)
                row += 1
            if len(callables) > 0:
                wx.CallAfter(self._process_callables, callables)

        self.SetInitialSize(self._WINDOW_SIZE)
        self.CenterOnParent()

    def get_settings(self):
        settings = {}
        for key in self._settings_controls.keys():
            settings[key] = self._settings_controls[key].GetValue().strip()
        return settings

    def clear_console(self):
        self._txt_console.Clear()

    def write_to_console(self, text):
        self._txt_console.AppendText("%s\n" % text)


if __name__ == "__main__":

    from tests.unit_tests.test_controller_edit_instrument import TestControllerEditInstrument

    TestControllerEditInstrument().run()
