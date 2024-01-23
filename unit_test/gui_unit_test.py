"""
Class with functions for GUI testing
"""

import time
import wx


class GuiUnitTest(object):

    KEY_TAB = 9
    KEY_ENTER = 13
    KEY_ESCAPE = 27

    _WAIT_TIMEOUT = 5

    ##########
    # Public #
    ##########

    @staticmethod
    def is_window_available(window_id):
        return wx.Window.FindWindowById(window_id) is not None

    @staticmethod
    def wait_until_window_available(window_id, timeout=_WAIT_TIMEOUT):
        while timeout > 0:
            wx.YieldIfNeeded()
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
        wx.YieldIfNeeded()

    @staticmethod
    def select_radio_button(button_id):
        ctrl = wx.Window.FindWindowById(button_id)
        ctrl.SetValue(True)
        wx.PostEvent(ctrl, wx.CommandEvent(wx.wxEVT_COMMAND_RADIOBUTTON_SELECTED, button_id))
        wx.YieldIfNeeded()

    @staticmethod
    def set_value_in_control(control_id, value):
        wx.Window.FindWindowById(control_id).SetValue(value)
        wx.YieldIfNeeded()

    @staticmethod
    def send_key_press(key_code, key_modifier=wx.MOD_NONE):
        ui = wx.UIActionSimulator()
        ui.Char(key_code, key_modifier)
        wx.YieldIfNeeded()

    @classmethod
    def send_text(cls, text, char_delay=0.001):
        for c in text:
            key_modifier = cls._determine_modifier_for_char(c)
            cls.send_key_press(ord(c), key_modifier)
            wx.YieldIfNeeded()
            time.sleep(char_delay)

    @classmethod
    def wait_for_dialog(cls, frame, break_if_dialog_present, timeout=2):
        while timeout > 0:
            if ((break_if_dialog_present and frame.active_dialog is not None) or
                    (not break_if_dialog_present and frame.active_dialog is None)):
                break
            time.sleep(0.2)
            timeout -= 0.2

    ###########
    # Private #
    ###########

    @staticmethod
    def _determine_modifier_for_char(c):
        if c in '~!@#$%^&*()_+{}:"<>?' or c.isupper():
            return wx.MOD_SHIFT
        return wx.MOD_NONE


if __name__ == "__main__":

    import threading


    class TestFrame(wx.Frame):

        ID_TEXT = wx.Window.NewControlId()
        ID_RADIO1 = wx.Window.NewControlId()
        ID_RADIO2 = wx.Window.NewControlId()
        ID_BUTTON_DIALOG = wx.Window.NewControlId()
        ID_BUTTON_CLOSE = wx.Window.NewControlId()

        _GAP = 5

        def __init__(self):
            super().__init__(None, wx.ID_ANY, "Test Frame")
            panel = wx.Panel(self)
            self.active_dialog = None

            self._text = wx.TextCtrl(panel, self.ID_TEXT, "Change this text", size=(300, -1))
            radio1 = wx.RadioButton(panel, self.ID_RADIO1, 'Radio button 1')
            radio1.Bind(wx.EVT_RADIOBUTTON, self._on_radio_button)
            radio2 = wx.RadioButton(panel, self.ID_RADIO2, 'Radio button 2')
            radio2.Bind(wx.EVT_RADIOBUTTON, self._on_radio_button)

            btn_dialog = wx.Button(panel, self.ID_BUTTON_DIALOG, "Show dialog")
            btn_dialog.Bind(wx.EVT_BUTTON, self._on_show_dialog_button)

            btn_close = wx.Button(panel, self.ID_BUTTON_CLOSE, "Close")
            btn_close.Bind(wx.EVT_BUTTON, self._on_close_button)

            box = wx.BoxSizer(wx.VERTICAL)
            box.Add(self._text, 0, wx.ALL, self._GAP)
            box.Add(radio1, 0, wx.ALL, self._GAP)
            box.Add(radio2, 0, wx.ALL, self._GAP)
            box.Add(btn_dialog, 0, wx.ALL, self._GAP)
            box.Add(btn_close, 0, wx.ALL, self._GAP)

            panel.SetSizer(box)
            self.SetInitialSize((400, 300))

        def _on_radio_button(self, event):
            self._text.SetValue("Radio ID: {}".format(event.GetId()))
            event.Skip()

        def _on_show_dialog_button(self, event):
            self.active_dialog = wx.MessageDialog(self, "Please close me.", "Dialog")
            self.active_dialog.ShowModal()
            self.active_dialog.Destroy()
            self.active_dialog = None
            event.Skip()

        def _on_close_button(self, event):
            self.Close()
            event.Skip()


    def test_thread(frame):
        print("Wait for GUI to be available")
        print("Is GUI available:", GuiUnitTest.is_window_available(TestFrame.ID_BUTTON_CLOSE))
        if GuiUnitTest.wait_until_window_available(TestFrame.ID_BUTTON_CLOSE):
            print("GUI is available")
            print("Is GUI available:", GuiUnitTest.is_window_available(TestFrame.ID_BUTTON_CLOSE))

            text = GuiUnitTest.get_value_from_window(TestFrame.ID_TEXT)
            print("Original text:", text)
            # Sleep so we can see the text changing
            time.sleep(1)

            print("Change text")
            GuiUnitTest.set_value_in_control(TestFrame.ID_TEXT, "And now for something completely different!")
            text = GuiUnitTest.get_value_from_window(TestFrame.ID_TEXT)
            print("New text:", text)
            # Sleep so we can see the text is changed
            time.sleep(1)

            print('Change text using send keys')
            GuiUnitTest.set_value_in_control(TestFrame.ID_TEXT, "")
            GuiUnitTest.send_text("I said: 'Ham, spam and bacon'! OK?", 0.02)
            text = GuiUnitTest.get_value_from_window(TestFrame.ID_TEXT)
            print("New text:", text)
            # Sleep so we can see the text is changed
            time.sleep(1)

            print("Toggle radio buttons")
            GuiUnitTest.select_radio_button(TestFrame.ID_RADIO2)
            text = GuiUnitTest.get_value_from_window(TestFrame.ID_TEXT)
            print("Active radio button:", text)
            time.sleep(1)

            GuiUnitTest.select_radio_button(TestFrame.ID_RADIO1)
            text = GuiUnitTest.get_value_from_window(TestFrame.ID_TEXT)
            print("Active radio button:", text)
            time.sleep(1)

            print("Click show dialog")
            GuiUnitTest.click_button(TestFrame.ID_BUTTON_DIALOG)
            GuiUnitTest.wait_for_dialog(frame, True)
            print("Dialog:", frame.active_dialog)
            time.sleep(1)
            if frame.active_dialog is not None:
                GuiUnitTest.send_key_press(GuiUnitTest.KEY_ENTER)
            time.sleep(1)

            print("Click the close button")
            GuiUnitTest.click_button(TestFrame.ID_BUTTON_CLOSE)


    app = wx.App(redirect=False)
    test_frame = TestFrame()

    t = threading.Thread(target=test_thread, args=(test_frame,))
    t.daemon = True
    t.start()

    test_frame.Show()
    app.MainLoop()
