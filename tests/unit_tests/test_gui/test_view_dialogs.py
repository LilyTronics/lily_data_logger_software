"""
Test the dialog widgets.
"""

import os
import wx

from src.views.view_dialogs import ViewDialogs
from tests.unit_tests.lib.test_suite import TestSuite


class TestViewDialogs(TestSuite):

    _app = None
    _test_frame = None
    _title = ""
    _error = ""
    _test_filename = ""

    class TestFrame(wx.Frame):

        def __init__(self):
            super().__init__(None)
            self.active_dialog = None

    def setup(self):
        self._app = self.gui.get_wx_app()
        self._test_frame = self.TestFrame()
        self._title = "Test dialogs"
        self._error = ""
        self._test_filename = os.path.abspath(__file__)

    def _check_dialog(self, test_id):
        self._error = ""
        self.gui.wait_for_dialog(self._test_frame)
        if self._test_frame.active_dialog is None:
            self._error = "No dialog was present"
        else:
            if test_id == 0:
                # We expect a message dialog
                self.gui.send_key_press(self.gui.KEY_ENTER)
            elif test_id in (1, 2):
                # We expect a confirm dialog that should be close with 'Yes' or 'No'
                if test_id == 2:
                    # Close with 'No'
                    self.gui.send_key_press(self.gui.KEY_TAB)
                self.gui.send_key_press(self.gui.KEY_ENTER)
            elif test_id in (3, 5):
                # We expect an open/save file dialog close with cancel
                self.gui.send_key_press(self.gui.KEY_ESCAPE)
            elif test_id in (4, 6):
                # We expect an open/save file dialog close with selecting a file
                # We need a sleep to make sure the dialog has the focus
                self.sleep(0.3)
                self.gui.send_text(self._test_filename)
                self.gui.send_key_press(self.gui.KEY_ENTER)

    def test_show_message(self):
        self.start_thread(self._check_dialog, args=(0, ))
        self.log.debug("Show message")
        ViewDialogs.show_message(self._test_frame, "This is a message dialog.", self._title)
        self.fail_if(self._error != "", self._error)

    def test_show_confirm(self):
        # Test 1: close with 'Yes'
        # Test 2: close with 'No'
        for i in range(1, 3):
            self.start_thread(self._check_dialog, args=(i, ))
            self.log.debug("Show confirm")
            button = ViewDialogs.show_confirm(self._test_frame, "This is a confirm dialog.",
                                              self._title)
            self.fail_if(self._error != "", self._error)
            self.fail_if(i == 1 and button != wx.ID_YES,
                         f"Expected return value {wx.ID_YES}, but got {button}")
            self.fail_if(i == 2 and button != wx.ID_NO,
                         f"Expected return value {wx.ID_NO}, but got {button}")

    def test_show_open_save_file(self):
        # Test 3: open file dialog close with 'Cancel
        # Test 4: open file dialog close with 'Open'
        # Test 5: save file dialog close with 'Cancel
        # Test 6: save file dialog close with 'Save'
        for i in range(3, 7):
            self.start_thread(self._check_dialog, args=(i,))
            if i < 5:
                self.log.debug("Show open file")
                filename = ViewDialogs.show_open_file(self._test_frame,
                                                      "This is a open file dialog.")
            else:
                self.log.debug("Show save file")
                filename = ViewDialogs.show_save_file(self._test_frame,
                                                      "This is a save file dialog.")
            self.fail_if(self._error != "", self._error)
            self.fail_if(i in (3, 5) and filename is not None,
                         f"Expected return value None, but got {filename}")
            self.fail_if(i in (4, 6) and filename != self._test_filename,
                         f"Expected return value {self._test_filename}, but got {filename}")

    def teardown(self):
        self._test_frame.Destroy()
        self._app.MainLoop()
        self._app.Destroy()
        del self._app


if __name__ == "__main__":

    import pylint

    TestViewDialogs().run()
    pylint.run_pylint([__file__])
