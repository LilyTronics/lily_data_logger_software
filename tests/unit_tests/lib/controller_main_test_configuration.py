"""
Configuration test for the main controller.
"""

import os
import tempfile
import wx

from src.models.configuration import Configuration
from src.models.id_manager import IdManager


class ControllerMainTestConfiguration(object):

    @classmethod
    def _open_edit_configuration(cls, test_suite):
        test_suite.gui.click_toolbar_item(test_suite.view_main, IdManager.ID_TOOL_EDIT_CONFIGURATION)
        if test_suite.gui.wait_until_window_available(IdManager.ID_END_TIME):
            return ""
        return "Edit configuration view did not appear"

    @staticmethod
    def _check_configuration_values(test_suite, sample_time, end_time, total_samples):
        wx.Yield()
        test_suite.sleep(0.2)
        value = test_suite.gui.get_value_from_window(IdManager.ID_LABEL_SAMPLE_TIME)
        if value != sample_time:
            return "The sample time does not have the correct value: '{}', expected '{}'".format(value, sample_time)
        value = test_suite.gui.get_value_from_window(IdManager.ID_LABEL_END_TIME)
        if value != end_time:
            return "The end time does not have the correct value: '{}', expected '{}'".format(value, end_time)
        # When continuous mode, total samples is not interesting
        if total_samples is not None:
            value = test_suite.gui.get_value_from_window(IdManager.ID_LABEL_TOTAL_SAMPLES)
            if value != total_samples:
                return "The total samples does not have the correct value: '{}', expected '{}'".format(value,
                                                                                                       total_samples)
        return ""

    @staticmethod
    def _close_main_view(test_suite, expect_dialog=True):
        result = ""
        test_suite.gui.post_event(test_suite.view_main, wx.wxEVT_CLOSE_WINDOW, test_suite.view_main.GetId())
        test_suite.log.debug("Check for configuration changed dialog")
        if test_suite.gui.wait_for_dialog(test_suite.view_main):
            if not expect_dialog:
                result += "\nConfiguration changed dialog did appear while we did not expect it"
            test_suite.gui.send_key_press(test_suite.gui.KEY_TAB)
            test_suite.gui.send_key_press(test_suite.gui.KEY_ENTER)
            if not test_suite.gui.wait_for_dialog(test_suite.view_main, False):
                result += "\nChanged configuration dialog did not close"
        elif expect_dialog:
            result += "\nConfiguration changed dialog did not appear"
        return result

    @classmethod
    def test_configuration_default_values(cls, test_suite):
        test_suite.log.debug("Check default configuration")
        result = cls._check_configuration_values(test_suite, "00:00:03", "00:01:00", "21")
        test_suite.view_main.Close()
        return result

    @classmethod
    def test_cancel_edit_configuration(cls, test_suite):
        test_suite.log.debug("Edit cancel configuration")
        result = cls._open_edit_configuration(test_suite)
        if result == "":
            test_suite.gui.set_value_in_control(IdManager.ID_SAMPLE_TIME, "5")
            test_suite.gui.set_value_in_control(IdManager.ID_END_TIME, "3")
            test_suite.gui.click_button(wx.ID_CANCEL)
            result = cls._check_configuration_values(test_suite, "00:00:03", "00:01:00", "21")
            result += cls._close_main_view(test_suite, False)
        return result

    @classmethod
    def test_edit_configuration_fixed_mode(cls, test_suite):
        test_suite.log.debug("Edit configuration fixed mode")
        result = cls._open_edit_configuration(test_suite)
        if result == "":
            test_suite.gui.set_value_in_control(IdManager.ID_SAMPLE_TIME, "5")
            test_suite.gui.set_value_in_control(IdManager.ID_END_TIME, "3")
            test_suite.gui.click_button(wx.ID_OK)
            result = cls._check_configuration_values(test_suite, "00:00:05", "00:03:00", "37")
            result += cls._close_main_view(test_suite)
        return result.strip()

    @classmethod
    def test_edit_configuration_continuous_mode(cls, test_suite):
        test_suite.log.debug("Edit configuration continuous mode")
        result = cls._open_edit_configuration(test_suite)
        if result == "":
            test_suite.gui.set_value_in_control(IdManager.ID_SAMPLE_TIME, "5")
            test_suite.gui.set_value_in_control(IdManager.ID_END_TIME, "3")
            test_suite.gui.select_radio_button(IdManager.ID_CONTINUOUS)
            test_suite.gui.click_button(wx.ID_OK)
            result = cls._check_configuration_values(test_suite, "00:00:05", "Continuous mode", None)
            result += cls._close_main_view(test_suite)
        return result

    @classmethod
    def test_open_configuration(cls, test_suite):
        test_suite.log.debug("Open configuration from file: {}".format(test_suite.configuration_test_filename))
        test_suite.gui.click_toolbar_item(test_suite.view_main, IdManager.ID_TOOL_OPEN_CONFIGURATION)
        test_suite.log.debug("Check for open configuration dialog")
        if test_suite.gui.wait_for_dialog(test_suite.view_main):
            test_suite.gui.send_text(test_suite.configuration_test_filename)
            test_suite.gui.send_key_press(test_suite.gui.KEY_ENTER)
            if not test_suite.gui.wait_for_dialog(test_suite.view_main, False):
                result = "Open configuration dialog did not close"
            else:
                result = cls._check_configuration_values(test_suite, "00:00:04", "00:05:00", "76")
        else:
            result = "No open configuration file dialog appeared"
        result += cls._close_main_view(test_suite)
        return result.strip()

    @classmethod
    def test_save_configuration(cls, test_suite):
        filename = tempfile.mktemp(suffix=".json")
        test_suite.log.debug("Change configuration before saving")
        result = cls._open_edit_configuration(test_suite)
        if result == "":
            test_suite.gui.set_value_in_control(IdManager.ID_SAMPLE_TIME, "5")
            test_suite.gui.set_value_in_control(IdManager.ID_END_TIME, "3")
            test_suite.gui.click_button(wx.ID_OK)
            result = cls._check_configuration_values(test_suite, "00:00:05", "00:03:00", "37")

        if result == "":
            test_suite.log.debug("Save configuration to file: {}".format(filename))
            test_suite.gui.click_toolbar_item(test_suite.view_main, IdManager.ID_TOOL_SAVE_CONFIGURATION)
            if test_suite.gui.wait_for_dialog(test_suite.view_main):
                test_suite.gui.send_text(filename)
                test_suite.gui.send_key_press(test_suite.gui.KEY_ENTER)
                if not test_suite.gui.wait_for_dialog(test_suite.view_main, False):
                    result = "Save configuration dialog did not close"
            else:
                result = "No save configuration file dialog appeared"

        if result == "":
            if not os.path.isfile(filename):
                result = "No file is created"
            else:
                test_suite.log.debug("Check values in the saved configuration file")
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

        result += cls._close_main_view(test_suite)
        return result.strip()


if __name__ == "__main__":

    from tests.unit_tests.test_controller_main import TestControllerMain

    TestControllerMain().run()
