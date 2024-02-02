"""
Dialog widgets.
"""

import glob
import os
import wx

from tests.test_suite import TestSuite


def show_message(parent, message, title, icon=wx.ICON_INFORMATION):
    parent.active_dialog = wx.MessageDialog(parent, message, title, wx.OK | icon)
    parent.active_dialog.ShowModal()
    parent.active_dialog.Destroy()
    parent.active_dialog = None


def show_confirm(parent, message, title, buttons=wx.YES | wx.NO):
    parent.active_dialog = wx.MessageDialog(parent, message, title, buttons | wx.ICON_QUESTION)
    button = parent.active_dialog.ShowModal()
    parent.active_dialog.Destroy()
    parent.active_dialog = None
    return button


def show_open_file(parent, message, default_folder="", default_file="", file_filter="All files|*.*"):
    selected_file = None
    parent.active_dialog = wx.FileDialog(parent, message, default_folder, default_file, file_filter, wx.FD_OPEN)
    if parent.active_dialog.ShowModal() == wx.ID_OK:
        selected_file = parent.active_dialog.GetPath()
    parent.active_dialog.Destroy()
    parent.active_dialog = None
    return selected_file


def show_save_file(parent, message, default_folder="", default_file="", file_filter="All files|*.*"):
    selected_file = None
    parent.active_dialog = wx.FileDialog(parent, message, default_folder, default_file, file_filter, wx.FD_SAVE)
    if parent.active_dialog.ShowModal() == wx.ID_OK:
        selected_file = parent.active_dialog.GetPath()
    parent.active_dialog.Destroy()
    parent.active_dialog = None
    return selected_file


class TestViewDialogs(TestSuite):

    class TestFrame(wx.Frame):

        def __init__(self):
            super().__init__(None)
            self.active_dialog = None

    def setup(self):
        self._app = wx.App(redirect=False)
        self._test_frame = self.TestFrame()
        self._title = "Test dialogs"
        self._error = ""
        self._test_filename = os.path.abspath(glob.glob(os.path.join(".", "*.py"))[0])
        print(self._test_filename)

    def _check_dialog(self, test_id):
        self._error = ""
        self.gui.wait_for_dialog(self._test_frame)
        if self._test_frame.active_dialog is None:
            self._error = "No dialog was present"
        else:
            if test_id == 0:
                # We expect a message dialog
                self.gui.send_key_press(self.gui.KEY_ENTER)
            elif test_id == 1 or test_id == 2:
                # We expect a confirm dialog that should be close with 'Yes' or 'No'
                if test_id == 2:
                    # Close with 'No'
                    self.gui.send_key_press(self.gui.KEY_TAB)
                self.gui.send_key_press(self.gui.KEY_ENTER)
            elif test_id == 3 or test_id == 5:
                # We expect an open/save file dialog close with cancel
                self.gui.send_key_press(self.gui.KEY_ESCAPE)
            elif test_id == 4 or test_id == 6:
                # We expect an open/save file dialog close with selecting a file
                # We need a sleep to make sure the dialog has the focus
                self.sleep(0.3)
                self.gui.send_text(self._test_filename)
                self.gui.send_key_press(self.gui.KEY_ENTER)

    def test_show_message(self):
        self.start_thread(self._check_dialog, args=(0, ))
        self.log.debug("Show message")
        show_message(self._test_frame, "This is a message dialog.", self._title)
        self.fail_if(self._error != "", self._error)

    def test_show_confirm(self):
        # Test 1: close with 'Yes'
        # Test 2: close with 'No'
        for i in range(1, 3):
            self.start_thread(self._check_dialog, args=(i, ))
            self.log.debug("Show confirm")
            button = show_confirm(self._test_frame, "This is a confirm dialog.", self._title)
            self.fail_if(self._error != "", self._error)
            self.fail_if(i == 1 and button != wx.ID_YES,
                         "Expected return value {}, but got {}".format(wx.ID_YES, button))
            self.fail_if(i == 2 and button != wx.ID_NO,
                         "Expected return value {}, but got {}".format(wx.ID_NO, button))

    def test_show_open_save_file(self):
        # Test 3: open file dialog close with 'Cancel
        # Test 4: open file dialog close with 'Open'
        # Test 5: save file dialog close with 'Cancel
        # Test 6: save file dialog close with 'Save'
        for i in range(3, 7):
            self.start_thread(self._check_dialog, args=(i,))
            if i < 5:
                self.log.debug("Show open file")
                filename = show_open_file(self._test_frame, "This is a open file dialog.")
            else:
                self.log.debug("Show save file")
                filename = show_save_file(self._test_frame, "This is a save file dialog.")
            self.fail_if(self._error != "", self._error)
            self.fail_if(i in [3, 5] and filename is not None,
                         "Expected return value None, but got {}".format(filename))
            self.fail_if(i in [4, 6] and filename != self._test_filename,
                         "Expected return value {}, but got {}".format(self._test_filename, filename))

    def teardown(self):
        self._test_frame.Destroy()
        self._app.MainLoop()


if __name__ == "__main__":

    TestViewDialogs().run()
