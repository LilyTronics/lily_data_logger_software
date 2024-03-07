"""
Just a window with a white background used as background when making screenshots
"""

import wx


class ViewWhite(wx.Frame):

    def __init__(self):
        super().__init__(None, wx.ID_ANY, "White screen")
        self.Maximize()
        panel = wx.Panel(self)
        panel.SetBackgroundColour("#fff")


app = wx.App(redirect=False)
ViewWhite().Show()
app.MainLoop()
