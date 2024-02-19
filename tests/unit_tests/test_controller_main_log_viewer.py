"""
Log viewer test for the main controller
"""

import wx

from src.models.id_manager import IdManager
from tests.unit_tests.test_controller_main import TestControllerMain


class TestControllerMainLogViewer(TestControllerMain):

    def _has_log_messages(self):
        return self.gui.get_value_from_window(IdManager.ID_LOG_MESSAGES) != ""

    @staticmethod
    def _get_log_view_object():
        matches = list(filter(lambda x: x.__class__.__name__ == "ViewLogger",
                              wx.GetTopLevelWindows()))
        if len(matches) == 1:
            return matches[0]
        return None

    def test_log_viewer(self):
        def _test_log_viewer():
            result = ""
            self.log.debug("Open log view")
            self.gui.click_toolbar_item(self.view_main, IdManager.ID_TOOL_SHOW_LOG)
            if self.gui.wait_until_window_available(IdManager.ID_LOG_MESSAGES):
                self.logger.debug("This is a test message")
                # The log view has a 300ms update rate
                self.log.debug("Check log messages")
                self.wait_for(self._has_log_messages, True, 1, 0.2)
                messages = self.gui.get_value_from_window(IdManager.ID_LOG_MESSAGES)
                if " | DEBUG  | This is a test message" not in messages:
                    result = "The log message was not shown in the log window"
                log_view = self._get_log_view_object()
                if log_view is None:
                    result = "Log window object not found"
                else:
                    self.log.debug("Close log view")
                    log_view.Close()
                    if not self.wait_for(self._get_log_view_object, None, 1, 0.1):
                        result = "The log window did not close"
                    else:
                        self.log.debug("Open log view again")
                        self.gui.click_toolbar_item(self.view_main, IdManager.ID_TOOL_SHOW_LOG)
                        if not self.gui.wait_until_window_available(IdManager.ID_LOG_MESSAGES):
                            result = "The log window did not appear"
            else:
                result = "The log window did not appear"
            self.log.debug("Close log view by closing the main view")
            self.view_main.Close()
            if not self.wait_for(self._get_log_view_object, None, 1, 0.1):
                result = "The log window did not close"
            return result

        self.show_view_main(_test_log_viewer)


if __name__ == "__main__":

    import pylint

    TestControllerMainLogViewer().run(True)
    pylint.run_pylint([__file__])
