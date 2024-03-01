"""
Test the progress dialog.
"""

import wx

from src.views.view_progress_dialog import ProgressDialog
from tests.unit_tests.lib.test_suite import TestSuite


class TestViewProgressDialog(TestSuite):

    _TITLE = "Test progress dialog"

    _error = ""
    _thread_time_out = 10

    class TestFrame(wx.Frame):

        def __init__(self):
            super().__init__(None)
            self.active_dialog = None

    def show_progress_dialog(self, test_function_to_run):
        def _test_thread(test_function):
            if not self.gui.wait_for_dialog(test_frame):
                self._error = "No dialog was present"
            else:
                self._error = test_function(test_frame)
                # Dialog must be closed after test
                if not self.gui.wait_for_dialog(test_frame, False):
                    self._error = "The dialog did not close"
                wx.CallAfter(test_frame.Close)

        self._error = ""
        app = self.gui.get_wx_app()
        test_frame = self.TestFrame()
        test_frame.Show()
        wx.CallAfter(ProgressDialog, test_frame, self._TITLE, 10)
        t = self.start_thread(_test_thread, (test_function_to_run,))
        app.MainLoop()
        self.wait_for(t.is_alive, False, self._thread_time_out, 0.1)
        self.gui.destroy_wx_app()
        self.fail_if(self._error != "", self._error.strip())

    def test_show_dialog(self):
        def _test_show_dialog(_):
            self.log.debug("Test show dialog")
            self.gui.send_key_press(self.gui.KEY_ENTER)
            return ""

        self.show_progress_dialog(_test_show_dialog)

    def test_progress(self):
        def _test_progress(test_frame):
            self.log.debug("Test progress")
            maximum = test_frame.active_dialog.GetRange() + 1
            for i in range(maximum):
                test_frame.active_dialog.update(i, f"Update {i}")
                self.sleep(0.1)
            return ""

        self.show_progress_dialog(_test_progress)

    def test_abort(self):
        def _test_abort(test_frame):
            self.log.debug("Test abort")
            maximum = test_frame.active_dialog.GetRange()
            for i in range(int(maximum / 2)):
                test_frame.active_dialog.update(i, f"Update {i}")
                self.sleep(0.1)
            # Dialog should not be closed
            if self.gui.wait_for_dialog(test_frame, False):
                return "The dialog closed"
            self.log.debug("Abort")
            self.gui.send_key_press(self.gui.KEY_ENTER)
            return ""

        self.show_progress_dialog(_test_abort)


if __name__ == "__main__":

    import pylint

    TestViewProgressDialog().run(True)
    pylint.run_pylint([__file__])
