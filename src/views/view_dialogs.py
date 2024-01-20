"""
Dialog widgets.
"""


import wx


def show_message(parent, message, title, icon=wx.ICON_INFORMATION):
    dlg = wx.MessageDialog(parent, message, title, wx.OK | icon)
    parent.active_dialog = dlg
    dlg.ShowModal()
    dlg.Destroy()
    parent.active_dialog = None


def show_confirm(parent, message, title, buttons=wx.YES | wx.NO):
    dlg = wx.MessageDialog(parent, message, title, buttons | wx.ICON_QUESTION)
    parent.active_dialog = dlg
    button = dlg.ShowModal()
    dlg.Destroy()
    parent.active_dialog = None
    return button


def show_open_file(parent, message, default_folder="", default_file="", file_filter="All files|*.*"):
    selected_file = None
    dlg = wx.FileDialog(parent, message, default_folder, default_file, file_filter, wx.FD_OPEN)
    parent.active_dialog = dlg
    if dlg.ShowModal() == wx.ID_OK:
        selected_file = dlg.GetPath()
    dlg.Destroy()
    parent.active_dialog = None
    return selected_file


def show_save_file(parent, message, default_folder="", default_file="", file_filter="All files|*.*"):
    selected_file = None
    dlg = wx.FileDialog(parent, message, default_folder, default_file, file_filter, wx.FD_SAVE)
    parent.active_dialog = dlg
    if dlg.ShowModal() == wx.ID_OK:
        selected_file = dlg.GetPath()
    dlg.Destroy()
    parent.active_dialog = None
    return selected_file


if __name__ == "__main__":

    class TestFrame(wx.Frame):

        def __init__(self):
            super().__init__(None)
            self.active_dialog = None

    _title = "Test Dialogs"

    app = wx.App(redirect=False)
    test_frame = TestFrame()

    _filename = show_open_file(test_frame, "Select a file")
    show_message(test_frame, "You selected: %s." % _filename, _title)

    _filename = show_save_file(test_frame, "Select a file")
    show_message(test_frame, "You selected: %s." % _filename, _title)

    _button = show_confirm(test_frame, "Press a button.", _title)
    show_message(test_frame, "You pressed button with ID: %s." % _button, _title)
