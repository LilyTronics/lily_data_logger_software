"""
Class with functions for GUI testing
"""

import wx


class GuiUnitTest(object):

    @staticmethod
    def is_window_available(window_id):
        return wx.Window.FindWindowById(window_id) is not None

    @staticmethod
    def get_value_from_window(window_id):
        value = wx.Window.FindWindowById(window_id)
        if value is not None:
            if hasattr(value, "GetValue"):
                value = value.GetValue()
            elif hasattr(value, "GetLabel"):
                value = value.GetLabel()
            else:
                raise Exception("Could not get value from window with ID {} ({})".format(window_id, value))
        return value

    @staticmethod
    def click_button(button_id):
        wx.PostEvent(wx.Window.FindWindowById(button_id), wx.CommandEvent(wx.wxEVT_COMMAND_BUTTON_CLICKED, button_id))
