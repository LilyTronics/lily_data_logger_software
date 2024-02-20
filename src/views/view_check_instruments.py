"""
View for checking instruments.
"""

import wx

from src.models.id_manager import IdManager


class ViewCheckInstruments(wx.Dialog):

    _LIST_COL_NAME_SIZE = 200
    _LIST_COL_STATUS_SIZE = 300
    _GAP = 5
    _COLOUR = {
        None: "#ffffff",
        False: "#ff8000",
        True: "#00ff80"
    }

    def __init__(self, parent):
        super().__init__(parent, wx.ID_ANY, "Check instruments")
        self.active_dialog = None

        self._lst_instruments = wx.ListCtrl(self, wx.ID_ANY,
                                            style=wx.LC_REPORT |wx.LC_SORT_ASCENDING |
                                            wx.LC_VRULES | wx.LC_HRULES)
        self._lst_instruments.InsertColumn(0, "Name", width=self._LIST_COL_NAME_SIZE)
        self._lst_instruments.InsertColumn(1, "Status", width=self._LIST_COL_STATUS_SIZE)
        btn_check = wx.Button(self, IdManager.ID_BTN_CHECK, "Check")

        box = wx.BoxSizer(wx.VERTICAL)
        box.Add(self._lst_instruments, 1, wx.EXPAND | wx.ALL, self._GAP)
        box.Add(btn_check, 0, wx.ALIGN_CENTER | wx.ALL, self._GAP)

        self.SetSizer(box)
        self.SetInitialSize((550, 300))
        self.CenterOnParent()

    ##########
    # Public #
    ##########

    def add_instruments(self, instrument_names):
        self._lst_instruments.DeleteAllItems()
        for instrument_name in instrument_names:
            item = wx.ListItem()
            item.SetId(self._lst_instruments.GetItemCount())
            item.SetText(instrument_name)
            self._lst_instruments.InsertItem(item)
        self._lst_instruments.SetColumnWidth(0, wx.LIST_AUTOSIZE)
        if self._lst_instruments.GetColumnWidth(0) < self._LIST_COL_NAME_SIZE:
            self._lst_instruments.SetColumnWidth(0, self._LIST_COL_NAME_SIZE)

    def update_instrument(self, instrument_name, is_passed, message):
        for i in range(self._lst_instruments.GetItemCount()):
            item = self._lst_instruments.GetItem(i, 0)
            if item.GetText() == instrument_name:
                self._lst_instruments.SetItemBackgroundColour(i, self._COLOUR[is_passed])
                self._lst_instruments.SetItem(i, 1, message)

                self._lst_instruments.SetColumnWidth(0, wx.LIST_AUTOSIZE)
                if self._lst_instruments.GetColumnWidth(0) < self._LIST_COL_NAME_SIZE:
                    self._lst_instruments.SetColumnWidth(0, self._LIST_COL_NAME_SIZE)
                self._lst_instruments.SetColumnWidth(1, wx.LIST_AUTOSIZE)
                if self._lst_instruments.GetColumnWidth(1) < self._LIST_COL_STATUS_SIZE:
                    self._lst_instruments.SetColumnWidth(1, self._LIST_COL_STATUS_SIZE)


if __name__ == "__main__":

    import pylint
    from tests.unit_tests.test_gui.test_controller_check_instruments import TestControllerCheckInstrument

    TestControllerCheckInstrument().run(True)
    pylint.run_pylint([__file__])
