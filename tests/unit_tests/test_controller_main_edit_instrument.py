"""
Test edit instrument for the main controller.
"""

import wx

from src.models.id_manager import IdManager
from tests.unit_tests.test_controller_main import TestControllerMain


class TestControllerMainEditInstrument(TestControllerMain):

    def _add_instrument(self):
        result = ""
        self.gui.click_button(IdManager.ID_BTN_ADD_INSTRUMENT)
        if not self.gui.wait_until_window_available(IdManager.ID_TEST_CONSOLE):
            result += "\nThe edit instrument dialog did not appear"
        else:
            self.log.debug("Add instrument")
            self.gui.set_value_in_control(IdManager.ID_INSTRUMENT_NAME, "Test instrument")
            self.gui.set_value_in_control(IdManager.ID_CMB_INSTRUMENT, "Simulator multimeter")
            self.gui.click_button(wx.ID_OK)
            self.log.debug("Check if instrument is in the list")
            list_control = self.gui.get_window(IdManager.ID_LIST_INSTRUMENTS)
            self.wait_for(list_control.GetItemCount, 1, 1, 0.1)
            if list_control.GetItemCount() < 1:
                result += "\nThe instrument is not in the list"
        return result

    def test_add_instrument(self):
        def _test_add_instrument():
            result = self._add_instrument()
            result += self.close_view_main(True)
            return result

        self.show_view_main(_test_add_instrument)

    def test_edit_instrument(self):
        def _test_edit_instrument():
            def _get_item_text():
                return list_control.GetItemText(0)

            result = self._add_instrument()
            if result == "":
                self.log.debug("Edit instrument")
                list_control = self.gui.get_window(IdManager.ID_LIST_INSTRUMENTS)
                list_control.Select(0)
                list_control.Focus(0)
                self.gui.send_key_press(self.gui.KEY_ENTER)
                if not self.gui.wait_until_window_available(IdManager.ID_TEST_CONSOLE):
                    result += "\nThe edit instrument dialog did not appear"
                else:
                    self.log.debug("Change name")
                    self.gui.set_value_in_control(IdManager.ID_INSTRUMENT_NAME,
                                                  "New instrument name")
                    self.gui.click_button(wx.ID_OK)
                    if not self.wait_for(_get_item_text, "New instrument name", 1, 0.1):
                        result += "\nWrong instrument name in the list"
            result += self.close_view_main(True)
            return result

        self.show_view_main(_test_edit_instrument)

    def test_delete_instrument(self):
        def _test_delete_instrument():
            result = self._add_instrument()
            if result == "":
                self.log.debug("Delete instrument")
                list_control = self.gui.get_window(IdManager.ID_LIST_INSTRUMENTS)
                list_control.Select(0)
                list_control.Focus(0)
                self.gui.click_button(IdManager.ID_BTN_DELETE_INSTRUMENT)
                if not self.gui.wait_for_dialog(self.view_main, True):
                    result += "\nThe dialog did not appear while we expected one"
                else:
                    self.gui.send_key_press(self.gui.KEY_ENTER)
                    if not self.wait_for(list_control.GetItemCount, 0, 1, 0.1):
                        result += "\nThe instrument was not removed from the list"
            result += self.close_view_main(True)
            return result

        self.show_view_main(_test_delete_instrument)

    def test_check_instruments(self):
        def _test_check_instruments():
            result = ""
            self.log.debug("Open check instruments dialog")
            self.gui.click_toolbar_item(self.view_main, IdManager.ID_TOOL_CHECK_INSTRUMENTS)
            if not self.gui.wait_until_window_available(IdManager.ID_BTN_CHECK):
                result = "The view check instruments did not appear"
            else:
                self.log.debug("Close check instruments dialog")
                view = self.gui.get_window(IdManager.ID_BTN_CHECK).GetParent()
                view.Close()
            self.view_main.Close()
            return result

        self.show_view_main(_test_check_instruments)


if __name__ == "__main__":

    import pylint

    TestControllerMainEditInstrument().run(True)
    pylint.run_pylint([__file__])
