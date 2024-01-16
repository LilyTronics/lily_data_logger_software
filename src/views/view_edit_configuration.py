"""
View for editing the configuration.
"""

import wx

from unit_test.test_suite import TestSuite


class ViewEditConfiguration(wx.Dialog):

    _GAP = 5
    _TIME_UNITS = ['seconds', 'minutes', 'hours', 'days']

    def __init__(self, parent):
        super(ViewEditConfiguration, self).__init__(parent, wx.ID_ANY, 'Edit Configuration')

        box = wx.BoxSizer(wx.VERTICAL)
        box.Add(self._create_time_settings_box(self), 0, wx.EXPAND | wx.ALL, self._GAP)
        box.Add(self._create_buttons_box(self), 0, wx.ALIGN_RIGHT | wx.ALL, self._GAP)

        self.SetSizer(box)
        self.SetInitialSize()
        self.CenterOnParent()

        self.Bind(wx.EVT_TEXT, self._on_time_change, self._txt_sample_time)
        self.Bind(wx.EVT_TEXT, self._on_time_change, self._txt_end_time)
        self.Bind(wx.EVT_COMBOBOX, self._on_time_change, self._cmb_sample_time)
        self.Bind(wx.EVT_COMBOBOX, self._on_time_change, self._cmb_end_time)
        self.Bind(wx.EVT_RADIOBUTTON, self._on_time_change, self._radio_end_time)
        self.Bind(wx.EVT_RADIOBUTTON, self._on_time_change, self._radio_continuous)

    def _create_time_settings_box(self, parent):
        box = wx.StaticBoxSizer(wx.StaticBox(parent, wx.ID_ANY, " Time settings: "), wx.VERTICAL)

        lbl_sample_time = wx.StaticText(parent, wx.ID_ANY, 'Sample time:')
        self._txt_sample_time = wx.TextCtrl(parent, wx.ID_ANY, size=(50, -1))
        self._cmb_sample_time = wx.ComboBox(parent, wx.ID_ANY, style=wx.CB_READONLY, choices=self._TIME_UNITS)
        self._radio_end_time = wx.RadioButton(parent, wx.ID_ANY, 'Fixed end time:')
        self._txt_end_time = wx.TextCtrl(parent, wx.ID_ANY, size=(50, -1))
        self._cmb_end_time = wx.ComboBox(parent, wx.ID_ANY, style=wx.CB_READONLY, choices=self._TIME_UNITS)
        self._radio_continuous = wx.RadioButton(parent, wx.ID_ANY, 'Continuous mode:')
        lbl_continuous = wx.StaticText(parent, wx.ID_ANY, 'Process must be stopped manually or by\n'
                                       'using the stop command in the process steps.')
        lbl_total_samples = wx.StaticText(parent, wx.ID_ANY, 'Total samples:')
        self._lbl_total_samples = wx.StaticText(parent, wx.ID_ANY, '-')

        grid = wx.GridBagSizer(self._GAP, self._GAP)
        grid.Add(lbl_sample_time, (0, 0), wx.DefaultSpan, wx.ALIGN_CENTER_VERTICAL)
        grid.Add(self._txt_sample_time, (0, 1), wx.DefaultSpan, wx.ALIGN_CENTER_VERTICAL)
        grid.Add(self._cmb_sample_time, (0, 2), wx.DefaultSpan, wx.ALIGN_CENTER_VERTICAL)
        grid.Add(self._radio_end_time, (1, 0), wx.DefaultSpan, wx.ALIGN_CENTER_VERTICAL)
        grid.Add(self._txt_end_time, (1, 1), wx.DefaultSpan, wx.ALIGN_CENTER_VERTICAL)
        grid.Add(self._cmb_end_time, (1, 2), wx.DefaultSpan, wx.ALIGN_CENTER_VERTICAL)
        grid.Add(self._radio_continuous, (2, 0), wx.DefaultSpan, wx.ALIGN_TOP)
        grid.Add(lbl_continuous, (2, 1), (1, 2), wx.ALIGN_TOP)
        grid.Add(lbl_total_samples, (3, 0), wx.DefaultSpan)
        grid.Add(self._lbl_total_samples, (3, 1), wx.DefaultSpan)

        box.Add(grid, 0, wx.EXPAND | wx.ALL, self._GAP)

        return box

    def _create_buttons_box(self, parent):
        btn_ok = wx.Button(parent, wx.ID_OK, 'Ok')
        btn_cancel = wx.Button(parent, wx.ID_CANCEL, 'Cancel')

        box = wx.BoxSizer(wx.HORIZONTAL)
        box.Add(btn_ok, 0, wx.ALL, self._GAP)
        box.Add(btn_cancel, 0, wx.ALL, self._GAP)

        return box

    ##################
    # Event handlers #
    ##################

    def _on_time_change(self, event):
        self._update_total_samples()
        event.Skip()

    ###########
    # Private #
    ###########

    @staticmethod
    def _convert_seconds_to_time(value):
        units = 'seconds'
        if value % 86400 == 0:
            units = 'days'
            value = int(value / 86400)
        elif value % 3600 == 0:
            units = 'hours'
            value = int(value / 3600)
        elif value % 60 == 0:
            units = 'minutes'
            value = int(value / 60)

        return value, units

    @staticmethod
    def _get_time(value_control, units_control):
        value = 0
        try:
            value = int(value_control.GetValue().strip())
        except ValueError:
            pass

        if value > 0:
            units = units_control.GetValue()
            if units == 'days':
                value *= 86400
            elif units == 'hours':
                value *= 3600
            elif units == 'minutes':
                value *= 60

        return value

    def _update_total_samples(self):
        total_samples = '-'
        if not self._radio_continuous.GetValue():
            sample_time = self._get_time(self._txt_sample_time, self._cmb_sample_time)
            end_time = self._get_time(self._txt_end_time, self._cmb_end_time)
            if sample_time > 0 and end_time > 0:
                total_samples = int(end_time / sample_time) + 1

        self._lbl_total_samples.SetLabel(str(total_samples))

    ##########
    # Public #
    ##########

    def get_sample_time(self):
        return self._get_time(self._txt_sample_time, self._cmb_sample_time)

    def set_sample_time(self, value):
        value, units = self._convert_seconds_to_time(value)
        self._txt_sample_time.SetValue(str(value))
        self._cmb_sample_time.SetValue(units)
        self._update_total_samples()

    def get_end_time(self):
        return self._get_time(self._txt_end_time, self._cmb_end_time)

    def set_end_time(self, value):
        value, units = self._convert_seconds_to_time(value)
        self._txt_end_time.SetValue(str(value))
        self._cmb_end_time.SetValue(units)
        self._update_total_samples()

    def get_continuous_mode(self):
        return self._radio_continuous.GetValue()

    def set_continuous_mode(self, value):
        self._radio_continuous.SetValue(value)
        self._radio_end_time.SetValue(not value)
        self._update_total_samples()


class TestViewEditConfiguration(TestSuite):

    _SHOW_VIEW = False

    def setup(self):
        self._app = wx.App(redirect=False)
        self._dlg = ViewEditConfiguration(None)

    def test_show_dialog(self):
        button = {
            wx.ID_OK: 'OK button',
            wx.ID_CANCEL: 'Cancel button'
        }
        if self._SHOW_VIEW:
            result = self._dlg.ShowModal()
            self.log.info('Dialog exit with code: {} ({})'.format(result, button[result]))

    def test_continuous_mode(self):
        self._dlg.set_sample_time(1)
        self._dlg.set_end_time(30)
        for mode in (True, False):
            self.log.debug('Set continuous mode {}'.format(mode))
            self._dlg.set_continuous_mode(mode)
            self.fail_if(self._dlg._radio_continuous.GetValue() != mode, 'Failed to set the continuous mode')
            self.fail_if(self._dlg._radio_end_time.GetValue() == mode, 'Failed to set the continuous mode')
            self.fail_if(mode and self._dlg._lbl_total_samples.GetLabel() != '-' or
                         not mode and self._dlg._lbl_total_samples.GetLabel() == '-',
                         'Total samples label has the wrong value')

    def test_time_values(self):
        time_values = (
            ((3, 40), ('3', 'seconds'), ('40', 'seconds'), '14'),
            ((120, 3000), ('2', 'minutes'), ('50', 'minutes'), '26'),
            ((14400, 72000), ('4', 'hours'), ('20', 'hours'), '6'),
            ((432000, 2592000), ('5', 'days'), ('30', 'days'), '7')
        )
        self._dlg.set_continuous_mode(False)
        for time_value in time_values:
            sample_time, end_time = time_value[0]
            self.log.debug('Set sample time to {} seconds ({} {})'.format(sample_time, *time_value[1]))
            self._dlg.set_sample_time(sample_time)
            self.log.debug('Set end time to {} seconds ({} {})'.format(end_time, *time_value[2]))
            self._dlg.set_end_time(end_time)
            self.fail_if(self._dlg._txt_sample_time.GetValue() != time_value[1][0],
                         'Wrong sample time value {}'.format(self._dlg._txt_sample_time.GetValue()))
            self.fail_if(self._dlg._cmb_sample_time.GetValue() != time_value[1][1],
                         'Wrong sample time units {}'.format(self._dlg._cmb_sample_time.GetValue()))
            self.fail_if(self._dlg._txt_end_time.GetValue() != time_value[2][0],
                         'Wrong end time value {}'.format(self._dlg._txt_end_time.GetValue()))
            self.fail_if(self._dlg._cmb_end_time.GetValue() != time_value[2][1],
                         'Wrong end time units {}'.format(self._dlg._cmb_end_time.GetValue()))
            self.fail_if(self._dlg._lbl_total_samples.GetLabel() != time_value[3],
                         'Wrong total samples {}'.format(self._dlg._lbl_total_samples.GetLabel()))
            self.fail_if(self._dlg.get_sample_time() != sample_time,
                         'Get sample time returned wrong value {}'.format(self._dlg.get_sample_time()))
            self.fail_if(self._dlg.get_end_time() != end_time,
                         'Get end time returned wrong value {}'.format(self._dlg.get_end_time()))

    def teardown(self):
        self._dlg.Destroy()


if __name__ == "__main__":

    TestViewEditConfiguration().run()
