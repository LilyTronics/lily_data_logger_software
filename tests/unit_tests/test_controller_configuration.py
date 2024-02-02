"""
Test for the controller configuration.
"""

import os
import tempfile
import wx

from src.controllers.controller_configuration import ControllerConfiguration
from src.models.configuration import Configuration
from src.models.id_manager import IdManager
from tests.unit_tests.lib.test_suite import TestSuite


class TestControllerConfiguration(TestSuite):

    def setup(self):
        self._filename = os.path.join(tempfile.gettempdir(), "test_config.json")
        self._app = wx.App(redirect=False)

    @staticmethod
    def _convert_seconds_to_time(value):
        units = "seconds"
        if value % 86400 == 0:
            units = "days"
            value = int(value / 86400)
        elif value % 3600 == 0:
            units = "hours"
            value = int(value / 3600)
        elif value % 60 == 0:
            units = "minutes"
            value = int(value / 60)
        return value, units

    def _get_time(self, value, units):
        if units == "days":
            value *= 86400
        elif units == "hours":
            value *= 3600
        elif units == "minutes":
            value *= 60
        elif units != "seconds":
            self.fail("The units are not correct: '{}'".format(units))
        return value

    def _get_values_from_view(self):
        return {
            "sample_time": self.gui.get_value_from_window(IdManager.ID_SAMPLE_TIME),
            "sample_time_units": self.gui.get_value_from_window(IdManager.ID_SAMPLE_TIME_UNITS),
            "end_time": self.gui.get_value_from_window(IdManager.ID_END_TIME),
            "end_time_units": self.gui.get_value_from_window(IdManager.ID_END_TIME_UNITS),
            "is_fixed": self.gui.get_value_from_window(IdManager.ID_FIXED),
            "is_continuous": self.gui.get_value_from_window(IdManager.ID_CONTINUOUS),
            "total_samples": self.gui.get_value_from_window(IdManager.ID_TOTAL_SAMPLES)
        }

    def _check_values_from_gui(self, conf):
        self.fail_if(self._values is None, 'No values from the GUI available')
        # Check the values from the GUI to the configuration values
        # Sample time with sample time units
        sample_time = self._get_time(float(self._values["sample_time"]), self._values["sample_time_units"])
        self.fail_if(sample_time != conf.get_sample_time(),
                     "Sample time does not have the correct value, is {} expected {}".format(
                        sample_time, conf.get_sample_time()))
        # End time with end time units
        end_time = self._get_time(float(self._values["end_time"]), self._values["end_time_units"])
        self.fail_if(end_time != conf.get_end_time(),
                     "End time does not have the correct value, is {} expected {}".format(
                         end_time, conf.get_end_time()))
        # Continuous mode
        self.fail_if(self._values["is_continuous"] != conf.get_continuous_mode(),
                     "Continuous mode does not have the correct value, is {} expected {}".format(
                         self._values["is_continuous"], conf.get_continuous_mode()))
        # Fixed mode
        self.fail_if(self._values["is_fixed"] == conf.get_continuous_mode(),
                     "Fixed edn time mode does not have the correct value, is {} expected {}".format(
                         self._values["is_fixed"], not conf.get_continuous_mode()))
        # Total samples, only with fixed end time
        if self._values["is_fixed"]:
            total_samples = int(end_time / sample_time) + 1
            self.fail_if(int(self._values["total_samples"]) != total_samples,
                         "Total samples does not have the correct value, is {} expected {}".format(
                             self._values["total_samples"], total_samples))
        else:
            self.fail_if(self._values["total_samples"] != "-",
                         "Total samples should be '-', but is {}".format(self._values["total_samples"]))

    def test_show_edit_configuration(self):
        def _test_show_edit_configuration():
            self.log.debug("Get default values")
            if self.gui.wait_until_window_available(IdManager.ID_SAMPLE_TIME):
                self._values = self._get_values_from_view()
                self.gui.click_button(wx.ID_CANCEL)

        self._values = None
        self.start_thread(_test_show_edit_configuration)
        conf = Configuration()
        ControllerConfiguration.edit_configuration(conf, None, self.log)
        self._check_values_from_gui(conf)
        wx.Yield()

    def test_edit_time_values(self):
        def _test_edit_time_values(time_value):
            if self.gui.wait_until_window_available(IdManager.ID_SAMPLE_TIME):
                time_value, units = self._convert_seconds_to_time(time_value)
                self.log.debug("Set time values to {} {}".format(time_value, units))
                self.gui.set_value_in_control(IdManager.ID_SAMPLE_TIME, str(time_value))
                self.gui.set_value_in_control(IdManager.ID_SAMPLE_TIME_UNITS, units)
                self.gui.set_value_in_control(IdManager.ID_END_TIME, str(time_value))
                self.gui.set_value_in_control(IdManager.ID_END_TIME_UNITS, units)
                self.gui.click_button(wx.ID_OK)

        for test_value in (23, 120, 14400, 172800):
            self.start_thread(_test_edit_time_values, (test_value, ))
            # Always start with default values
            conf = Configuration()
            ControllerConfiguration.edit_configuration(conf, None, self.log)
            self.fail_if(test_value != conf.get_sample_time(),
                         "The sample time is not correct, is {} expected {}".format(conf.get_sample_time(), test_value))
            self.fail_if(test_value != conf.get_end_time(),
                         "The end time is not correct, is {} expected {}".format(conf.get_end_time(), test_value))
            wx.Yield()

    def test_edit_continuous_mode(self):
        def _test_edit_continuous_mode(test_mode):
            self.log.debug("Set continuous mode to {}".format(test_mode))
            if self.gui.wait_until_window_available(IdManager.ID_CONTINUOUS):
                if test_mode:
                    self.gui.select_radio_button(IdManager.ID_CONTINUOUS)
                else:
                    self.gui.select_radio_button(IdManager.ID_FIXED)
                # Wait for total samples to change, should be fast
                t = 1
                while t > 0:
                    self._total_samples = self.gui.get_value_from_window(IdManager.ID_TOTAL_SAMPLES)
                    if test_mode and self._total_samples == '-' or not test_mode and self._total_samples != '-':
                        break
                    self.sleep(0.1)
                    t -= 0.1
                self.gui.click_button(wx.ID_OK)

        self._total_samples = None
        conf = Configuration()
        for mode in (True, False):
            self.start_thread(_test_edit_continuous_mode, (mode,))
            ControllerConfiguration.edit_configuration(conf, None, self.log)
            self.fail_if(conf.get_continuous_mode() != mode,
                         "Continuous mode is not correct, is {} should be {}".format(conf.get_continuous_mode(), mode))
            if mode:
                self.fail_if(self._total_samples != "-",
                             "Total samples should be '-', but got '{}'".format(self._total_samples))
            else:
                self.fail_if(self._total_samples == "-",
                             "Total samples should be a number, but got '{}'".format(self._total_samples))
            wx.Yield()

    def test_configuration_is_changed(self):
        def _test_configuration_is_changed(test, frame):
            self.gui.wait_for_dialog(frame)
            if test == 1:
                if frame.active_dialog is not None:
                    self._error = "A dialog was shown when not expected"
                    # Close the dialog
                    self.gui.send_key_press(self.gui.KEY_TAB)
                    self.gui.send_key_press(self.gui.KEY_ENTER)
                    self.gui.wait_for_dialog(frame, False)
                return
            if test > 1 and frame.active_dialog is None:
                self._error = "No dialog was shown when expected"
                return
            # A dialog is shown, as expected
            if test == 2:
                # Close with no button, we expect no new dialog
                self.gui.send_key_press(self.gui.KEY_TAB)
                self.gui.send_key_press(self.gui.KEY_ENTER)
                self.gui.wait_for_dialog(frame, False)
            elif test == 3:
                # Click Yes button, there must be a save file dialog
                self.gui.send_key_press(self.gui.KEY_ENTER)
                # Wait for message dialog to be gone
                self.gui.wait_for_dialog(frame, False)
                # Wait for file dialog
                self.gui.wait_for_dialog(frame)
                # Send escape to close the file dialog
                self.gui.send_key_press(self.gui.KEY_ESCAPE)
                # Wait for dialog to be gone
                self.gui.wait_for_dialog(frame, False)

        # Test 1: no change
        # Test 2: is changed, no save
        # Test 3: is changed, do save
        for test_id in range(1, 4):
            self._error = ""
            test_frame = wx.Frame(None)
            test_frame.active_dialog = None
            conf = Configuration()
            if test_id == 1:
                self.log.debug("Test when configuration is not changed (expecting no dialogs)")
            else:
                self.log.debug("Test when configuration is changed (expecting dialogs)")
                conf.set_sample_time(conf.get_sample_time() + 1)
            t = self.start_thread(_test_configuration_is_changed, (test_id, test_frame))
            ControllerConfiguration.check_configuration_is_changed(conf, test_frame, self.log)
            while t.is_alive():
                self.sleep(0.1)
            test_frame.Destroy()
            wx.Yield()
            self.fail_if(self._error != "", self._error)

    def test_save_configuration(self):
        def _test_save_configuration(frame):
            if not self.gui.wait_for_dialog(frame):
                self._error = "No dialog was shown when expected"
                return
            self.log.debug("Save configuration to {}".format(self._filename))
            self.gui.send_text(self._filename)
            self.gui.send_key_press(self.gui.KEY_ENTER)

        self._error = ""
        test_frame = wx.Frame(None)
        test_frame.active_dialog = None
        conf = Configuration()
        conf.set_sample_time(2)
        conf.set_end_time(120)
        self.start_thread(_test_save_configuration, (test_frame, ))
        ControllerConfiguration.save_to_file(conf, test_frame, self.log)
        test_frame.Destroy()
        wx.Yield()
        self.fail_if(self._error != "", self._error)

    def test_load_configuration(self):
        def _test_load_configuration(frame):
            if not self.gui.wait_for_dialog(frame):
                self._error = "No dialog was shown when expected"
                return
            self.log.debug("Load configuration from {}".format(self._filename))
            self.gui.send_text(self._filename)
            self.gui.send_key_press(self.gui.KEY_ENTER)

        self._error = ""
        test_frame = wx.Frame(None)
        test_frame.active_dialog = None
        conf = Configuration()
        self.start_thread(_test_load_configuration, (test_frame,))
        ControllerConfiguration.load_from_file(conf, test_frame, self.log)
        test_frame.Destroy()
        wx.Yield()
        self.fail_if(self._error != "", self._error)
        self.fail_if(conf.get_sample_time() != 2, "Sample time is not loaded from the file")
        self.fail_if(conf.get_end_time() != 120, "Sample time is not loaded from the file")

    def teardown(self):
        self._app.MainLoop()
        if os.path.isfile(self._filename):
            os.remove(self._filename)


if __name__ == "__main__":

    TestControllerConfiguration().run()
