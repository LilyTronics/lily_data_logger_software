"""
Configuration test for the main controller.
"""

import os
import tempfile
import wx

from src.models.configuration import Configuration
from src.models.id_manager import IdManager
from tests.unit_tests.test_controller_main import TestControllerMain


class TestControllerMainConfiguration(TestControllerMain):

    def _check_configuration_values(self, sample_time, end_time, total_samples):
        self.sleep(0.2)
        value = self.gui.get_value_from_window(IdManager.ID_LABEL_SAMPLE_TIME)
        if value != sample_time:
            return "The sample time does not have the correct value: '{}', expected '{}'".format(value, sample_time)
        value = self.gui.get_value_from_window(IdManager.ID_LABEL_END_TIME)
        if value != end_time:
            return "The end time does not have the correct value: '{}', expected '{}'".format(value, end_time)
        # When continuous mode, total samples is not interesting
        if total_samples is not None:
            value = self.gui.get_value_from_window(IdManager.ID_LABEL_TOTAL_SAMPLES)
            if value != total_samples:
                return "The total samples does not have the correct value: '{}', expected '{}'".format(
                    value, total_samples)
        return ""

    def _open_edit_configuration(self):
        self.gui.click_toolbar_item(self.view_main, IdManager.ID_TOOL_EDIT_CONFIGURATION)
        if self.gui.wait_until_window_available(IdManager.ID_END_TIME):
            return ""
        return "Edit configuration view did not appear"

    def test_configuration_default_values(self):
        def _test_configuration_default_values():
            self.log.debug("Check default configuration")
            result = self._check_configuration_values("00:00:03", "00:01:00", "21")
            result += self.close_view_main(False)
            return result

        self.show_view_main(_test_configuration_default_values)

    def test_cancel_edit_configuration(self):
        def _test_cancel_edit_configuration():
            self.log.debug("Edit cancel configuration")
            result = self._open_edit_configuration()
            if result == "":
                self.gui.set_value_in_control(IdManager.ID_SAMPLE_TIME, "5")
                self.gui.set_value_in_control(IdManager.ID_END_TIME, "3")
                self.gui.click_button(wx.ID_CANCEL)
                result = self._check_configuration_values("00:00:03", "00:01:00", "21")
                result += self.close_view_main(False)
            return result

        self.show_view_main(_test_cancel_edit_configuration)

    def test_edit_configuration_fixed_mode(self):
        def _test_edit_configuration_fixed_mode():
            self.log.debug("Edit configuration fixed mode")
            result = self._open_edit_configuration()
            if result == "":
                self.gui.set_value_in_control(IdManager.ID_SAMPLE_TIME, "5")
                self.gui.set_value_in_control(IdManager.ID_END_TIME, "3")
                self.gui.click_button(wx.ID_OK)
                result = self._check_configuration_values("00:00:05", "00:03:00", "37")
                result += self.close_view_main(True)
            return result

        self.show_view_main(_test_edit_configuration_fixed_mode)

    def test_edit_configuration_continuous_mode(self):
        def _test_edit_configuration_continuous_mode():
            self.log.debug("Edit configuration continuous mode")
            result = self._open_edit_configuration()
            if result == "":
                self.gui.set_value_in_control(IdManager.ID_SAMPLE_TIME, "5")
                self.gui.set_value_in_control(IdManager.ID_END_TIME, "3")
                self.gui.select_radio_button(IdManager.ID_CONTINUOUS)
                self.gui.click_button(wx.ID_OK)
                result = self._check_configuration_values("00:00:05", "Continuous mode", None)
                result += self.close_view_main(True)
            return result

        self.show_view_main(_test_edit_configuration_continuous_mode)

    def test_open_configuration(self):
        def _test_open_configuration():
            self.log.debug("Open configuration from file: {}".format(self.configuration_test_filename))
            self.gui.click_toolbar_item(self.view_main, IdManager.ID_TOOL_OPEN_CONFIGURATION)
            self.log.debug("Check for open configuration dialog")
            if self.gui.wait_for_dialog(self.view_main):
                self.gui.send_text(self.configuration_test_filename)
                self.gui.send_key_press(self.gui.KEY_ENTER)
                if not self.gui.wait_for_dialog(self.view_main, False):
                    result = "Open configuration dialog did not close"
                else:
                    result = self._check_configuration_values("00:00:04", "00:05:00", "76")
                    list_control = self.gui.get_window(IdManager.ID_LIST_INSTRUMENTS)
                    self.wait_for(list_control.GetItemCount, 1, 1, 0.1)
                    if list_control.GetItemCount() < 1:
                        result += "The instrument is not in the list"
            else:
                result = "No open configuration file dialog appeared"
            result += self.close_view_main(False)
            return result.strip()

        self.show_view_main(_test_open_configuration)

    def test_save_configuration(self):
        def _test_save_configuration():
            filename = tempfile.mktemp(suffix=".json")
            self.log.debug("Change configuration before saving")
            result = self._open_edit_configuration()
            if result == "":
                self.gui.set_value_in_control(IdManager.ID_SAMPLE_TIME, "5")
                self.gui.set_value_in_control(IdManager.ID_END_TIME, "3")
                self.gui.click_button(wx.ID_OK)
                result = self._check_configuration_values("00:00:05", "00:03:00", "37")
            if result == "":
                self.log.debug("Save configuration to file: {}".format(filename))
                self.gui.click_toolbar_item(self.view_main, IdManager.ID_TOOL_SAVE_CONFIGURATION)
                if self.gui.wait_for_dialog(self.view_main):
                    self.gui.send_text(filename)
                    self.gui.send_key_press(self.gui.KEY_ENTER)
                    if not self.gui.wait_for_dialog(self.view_main, False):
                        result = "Save configuration dialog did not close"
                else:
                    result = "No save configuration file dialog appeared"
            if result == "":
                if not os.path.isfile(filename):
                    result = "No file is created"
                else:
                    self.log.debug("Check values in the saved configuration file")
                    conf = Configuration()
                    conf.load_from_file(filename)
                    if conf.get_sample_time() != 5:
                        result = "Sample time was not saved correct: {}, expected 5".format(conf.get_sample_time())
                    if result == "" and conf.get_end_time() != 180:
                        result = "End time was not saved correct: {}, expected 180".format(conf.get_end_time())
                    if result == "" and conf.get_continuous_mode():
                        result = "Continuous mode was not saved correct: {}, expected False".format(
                            conf.get_continuous_mode())
            if os.path.isfile(filename):
                os.remove(filename)
            result += self.close_view_main(False)
            return result

        self.show_view_main(_test_save_configuration)


if __name__ == "__main__":

    TestControllerMainConfiguration().run(True)
