"""
Dialog widgets.
"""


import wx


def show_message(parent, message, title, icon=wx.ICON_INFORMATION):
    dlg = wx.MessageDialog(parent, message, title, wx.OK | icon)
    dlg.ShowModal()
    dlg.Destroy()


def show_confirm(parent, message, title, buttons=wx.YES | wx.NO):
    dlg = wx.MessageDialog(parent, message, title, buttons | wx.ICON_QUESTION)
    button = dlg.ShowModal()
    dlg.Destroy()
    return button


def show_open_file(parent, message, default_folder="", default_file="", file_filter="All files|*.*"):
    selected_file = None
    dlg = wx.FileDialog(parent, message, default_folder, default_file, file_filter, wx.FD_OPEN)
    if dlg.ShowModal() == wx.ID_OK:
        selected_file = dlg.GetPath()
    dlg.Destroy()
    return selected_file


def show_save_file(parent, message, default_folder="", default_file="", file_filter="All files|*.*"):
    selected_file = None
    dlg = wx.FileDialog(parent, message, default_folder, default_file, file_filter, wx.FD_SAVE)
    if dlg.ShowModal() == wx.ID_OK:
        selected_file = dlg.GetPath()
    dlg.Destroy()
    return selected_file


if __name__ == "__main__":

    _title = "Test Dialogs"

    app = wx.App(redirect=False)

    _filename = show_open_file(None, "Select a file")
    show_message(None, "You selected: %s." % _filename, _title)

    _filename = show_save_file(None, "Select a file")
    show_message(None, "You selected: %s." % _filename, _title)

    _button = show_confirm(None, "Press a button.", _title)
    show_message(None, "You pressed button with ID: %s." % _button, _title)
