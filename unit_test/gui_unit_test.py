"""
Class with functions for GUI testing
"""

import time
import wx


class GuiUnitTest(object):

    _WAIT_TIMEOUT = 5

    @staticmethod
    def is_window_available(window_id):
        return wx.Window.FindWindowById(window_id) is not None

    @staticmethod
    def wait_until_window_available(window_id, timeout=_WAIT_TIMEOUT):
        while timeout > 0:
            wx.Yield()
            if wx.Window.FindWindowById(window_id) is not None:
                # Even though it is available, we need to wait a bit to have full access to all properties
                time.sleep(0.1)
                return True
            time.sleep(0.05)
            timeout -= 0.05
        return False

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

    @staticmethod
    def set_value_in_control(control_id, value):
        wx.Window.FindWindowById(control_id).SetValue(value)


if __name__ == "__main__":

    import threading


    class TestFrame(wx.Frame):

        ID_TEXT = 101
        ID_RADIO1 = 102
        ID_RADIO2 = 103
        ID_BUTTON = 201

        _GAP = 5

        def __init__(self):
            super().__init__(None, wx.ID_ANY, "Test Frame")
            panel = wx.Panel(self)

            text = wx.TextCtrl(panel, self.ID_TEXT, "Change this text", size=(300, -1))
            radio1 = wx.RadioButton(panel, self.ID_RADIO1, 'Radio button 1')
            radio2 = wx.RadioButton(panel, self.ID_RADIO2, 'Radio button 2')
            btn = wx.Button(panel, self.ID_BUTTON, "Close")
            btn.Bind(wx.EVT_BUTTON, self._on_close_button)

            box = wx.BoxSizer(wx.VERTICAL)
            box.Add(text, 0, wx.ALL, self._GAP)
            box.Add(radio1, 0, wx.ALL, self._GAP)
            box.Add(radio2, 0, wx.ALL, self._GAP)
            box.Add(btn, 0, wx.ALL, self._GAP)

            panel.SetSizer(box)
            self.SetInitialSize((400, 300))

        def _on_close_button(self, event):
            self.Close()
            event.Skip()


    def test_thread():
        print("Wait for GUI to be available")
        print("Is GUI available:", GuiUnitTest.is_window_available(TestFrame.ID_BUTTON))
        if GuiUnitTest.wait_until_window_available(TestFrame.ID_BUTTON):
            print("GUI is available")
            print("Is GUI available:", GuiUnitTest.is_window_available(TestFrame.ID_BUTTON))
            org_text = GuiUnitTest.get_value_from_window(TestFrame.ID_TEXT)
            print("Original text:", org_text)
            # Sleep so we can see the text changing
            time.sleep(1)
            print("Change text")
            GuiUnitTest.set_value_in_control(TestFrame.ID_TEXT, "And now for something completely different!")
            # Sleep so we can see the text is changed
            time.sleep(1)
            new_text = GuiUnitTest.get_value_from_window(TestFrame.ID_TEXT)
            if new_text != org_text:
                print("Yes! Text has changed")
            else:
                print("Oops... text is not changed :(")
            print("Toggle radio buttons")
            GuiUnitTest.set_value_in_control(TestFrame.ID_RADIO2, True)
            time.sleep(1)
            GuiUnitTest.set_value_in_control(TestFrame.ID_RADIO1, True)
            time.sleep(1)
            GuiUnitTest.click_button(TestFrame.ID_BUTTON)


    t = threading.Thread(target=test_thread)
    t.daemon = True
    t.start()

    app = wx.App(redirect=False)
    TestFrame().Show()
    app.MainLoop()
