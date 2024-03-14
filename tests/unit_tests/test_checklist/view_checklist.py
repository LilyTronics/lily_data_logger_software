"""
Release checklist.
"""

import wx


class ViewCheckList(wx.Frame):

    _GAP = 10
    _REMARKS_SIZE = (200, -1)
    _INITIAL_WIDTH = 500

    def __init__(self, test_items, app_version, check_callback):
        self._remarks = []
        self._check = []
        self._check_callback = check_callback
        super().__init__(None, wx.ID_ANY, f"Release Checklist - Application V{app_version}")
        panel = wx.Panel(self)

        grid = wx.GridBagSizer(self._GAP, self._GAP)
        grid.Add(wx.StaticText(panel, wx.ID_ANY, "Test"), (0, 0), wx.DefaultSpan)
        grid.Add(wx.StaticText(panel, wx.ID_ANY, "Result"), (0, 1), wx.DefaultSpan,
                 wx.ALIGN_CENTER_HORIZONTAL)
        grid.Add(wx.StaticText(panel, wx.ID_ANY, "Remarks"), (0, 2), wx.DefaultSpan)
        for i, item in enumerate(test_items):
            lbl = wx.StaticText(panel, wx.ID_ANY, item["label"])
            if item["type"] is bool:
                ctrl = wx.CheckBox(panel, wx.ID_ANY)
            else:
                ctrl = wx.StaticText(panel, wx.ID_ANY, f"Invalid type: {item["type"]}")
            self._check.append(ctrl)
            self._remarks.append(wx.TextCtrl(panel, wx.ID_ANY, "", size=self._REMARKS_SIZE))
            row = i + 1
            grid.Add(lbl, (row, 0), wx.DefaultSpan, wx.EXPAND | wx.ALIGN_CENTER_VERTICAL)
            grid.Add(self._check[i], (row, 1), wx.DefaultSpan, wx.EXPAND | wx.ALIGN_CENTER)
            grid.Add(self._remarks[i], (row, 2), wx.DefaultSpan,
                     wx.EXPAND | wx.ALIGN_CENTER_VERTICAL)
        grid.AddGrowableCol(0)

        btn = wx.Button(panel, wx.ID_ANY, "Check")
        btn.Bind(wx.EVT_BUTTON, self._on_check)
        self._chk_open_in_browser = wx.CheckBox(panel, wx.ID_ANY, "Open report in browser")

        button_box = wx.BoxSizer(wx.HORIZONTAL)
        button_box.Add(btn, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, self._GAP)
        button_box.Add(self._chk_open_in_browser, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, self._GAP)

        box = wx.BoxSizer(wx.VERTICAL)
        box.Add(grid, 1, wx.EXPAND | wx.ALL, self._GAP)
        box.Add(button_box, 0, wx.CENTER | wx.ALL, self._GAP)
        panel.SetSizer(box)
        height = 120
        if len(test_items) > 0:
            height += len(test_items) * (self._remarks[0].GetSize()[1] + self._GAP)
        self.SetInitialSize((self._INITIAL_WIDTH, height))

    ##################
    # Event handlers #
    ##################

    def _on_check(self, event):
        self._check_callback(self._check, self._remarks, self._chk_open_in_browser.GetValue())
        event.Skip()


if __name__ == "__main__":

    _test_items = [
        {"label": "Test item boolean", "type": bool, "pass_if": True, "result": None},
    ]

    def _check_callback(*args):
        print(args)

    app = wx.App(redirect=False)
    ViewCheckList(_test_items, "99.99", _check_callback).Show()
    app.MainLoop()
