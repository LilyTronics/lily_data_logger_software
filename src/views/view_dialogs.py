"""
Dialog widgets.
"""

import wx


class ViewDialogs:

    @staticmethod
    def show_message(parent, message, title, icon=wx.ICON_INFORMATION):
        parent.active_dialog = wx.MessageDialog(parent, message, title, wx.OK | icon)
        parent.active_dialog.ShowModal()
        parent.active_dialog.Destroy()
        parent.active_dialog = None

    @staticmethod
    def show_confirm(parent, message, title, buttons=wx.YES | wx.NO):
        parent.active_dialog = wx.MessageDialog(parent, message, title, buttons | wx.ICON_QUESTION)
        button = parent.active_dialog.ShowModal()
        parent.active_dialog.Destroy()
        parent.active_dialog = None
        return button

    @staticmethod
    def show_open_file(parent, message, default_folder="", default_file="",
                       file_filter="All files|*.*"):
        selected_file = None
        parent.active_dialog = wx.FileDialog(parent, message, default_folder, default_file,
                                             file_filter, wx.FD_OPEN)
        if parent.active_dialog.ShowModal() == wx.ID_OK:
            selected_file = parent.active_dialog.GetPath()
        parent.active_dialog.Destroy()
        parent.active_dialog = None
        return selected_file

    @staticmethod
    def show_save_file(parent, message, default_folder="", default_file="",
                       file_filter="All files|*.*"):
        selected_file = None
        parent.active_dialog = wx.FileDialog(parent, message, default_folder, default_file,
                                             file_filter, wx.FD_SAVE)
        if parent.active_dialog.ShowModal() == wx.ID_OK:
            selected_file = parent.active_dialog.GetPath()
        parent.active_dialog.Destroy()
        parent.active_dialog = None
        return selected_file


if __name__ == "__main__":

    from tests.unit_tests.test_gui.test_view_dialogs import TestViewDialogs

    TestViewDialogs().run()
