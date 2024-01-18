"""
Controller for handling the configuration.
"""

import wx

from src.models.configuration import Configuration
from src.views.view_dialogs import show_confirm
from src.views.view_dialogs import show_message
from src.views.view_dialogs import show_open_file
from src.views.view_dialogs import show_save_file
from src.views.view_edit_configuration import ViewEditConfiguration
from unit_test.test_suite import TestSuite


class ControllerConfiguration(object):

    _FILE_FILTER = "Configuration files (*.json)|*.json"

    @classmethod
    def check_configuration_is_changed(cls, configuration, parent_view, logger):
        if configuration.is_changed():
            btn = show_confirm(parent_view, "The configuration is changed. Save configuration?", "Save configuration")
            if btn == wx.ID_YES:
                cls.save_to_file(configuration, parent_view, logger)

    @classmethod
    def load_from_file(cls, configuration, parent_view, logger):
        dlg_title = "Open configuration"
        cls.check_configuration_is_changed(configuration, parent_view, logger)
        filename = show_open_file(parent_view, dlg_title, file_filter=cls._FILE_FILTER)
        if filename is not None:
            logger.debug("Load configuration from file: {}".format(filename))
            try:
                configuration.load_from_file(filename)
            except Exception as e:
                logger.error(str(e))
                show_message(parent_view, "Error when reading file {}:\n{}".format(filename, e), dlg_title)

    @classmethod
    def save_to_file(cls, configuration, parent_view, logger):
        dlg_title = "Save configuration"
        filename = show_save_file(parent_view, dlg_title, file_filter=cls._FILE_FILTER)
        if filename is not None:
            logger.debug("Save configuration to file: {}".format(filename))
            try:
                configuration.save_to_file(filename)
            except Exception as e:
                logger.error(str(e))
                show_message(parent_view, "Error when writing file {}:\n{}".format(filename, e), dlg_title)

    @classmethod
    def edit_configuration(cls, configuration, parent_view, logger):
        dlg = ViewEditConfiguration(parent_view)
        dlg.set_sample_time(configuration.get_sample_time())
        dlg.set_end_time(configuration.get_end_time())
        dlg.set_continuous_mode(configuration.get_continuous_mode())
        if dlg.ShowModal() == wx.ID_OK:
            logger.info("Edit configuration settings")
            current_sample_time = configuration.get_sample_time()
            new_sample_time = dlg.get_sample_time()
            if current_sample_time != new_sample_time:
                configuration.set_sample_time(new_sample_time)
                logger.debug("Sample time changed from {} to {} seconds".format(current_sample_time, new_sample_time))
            current_end_time = configuration.get_end_time()
            new_end_time = dlg.get_end_time()
            if current_end_time != new_end_time:
                configuration.set_end_time(new_end_time)
                logger.debug("End time changed from {} to {} seconds".format(current_end_time, new_end_time))
            current_continuous_mode = configuration.get_continuous_mode()
            new_continuous_mode = dlg.get_continuous_mode()
            if current_continuous_mode != new_continuous_mode:
                configuration.set_continuous_mode(new_continuous_mode)
                logger.debug("Continuous mode changed from {} to {}".format(current_continuous_mode,
                                                                            new_continuous_mode))
        dlg.Destroy()


class TestControllerConfiguration(TestSuite):

    def setup(self):
        self._conf = Configuration()
        self._app = wx.App(redirect=False)
        self._values = None

    def _get_values_from_view(self):
        return {
            "sample_time": self.gui.get_value_from_window(ViewEditConfiguration.ID_SAMPLE_TIME),
            "sample_time_units": self.gui.get_value_from_window(ViewEditConfiguration.ID_SAMPLE_TIME_UNITS),
            "end_time": self.gui.get_value_from_window(ViewEditConfiguration.ID_END_TIME),
            "end_time_units": self.gui.get_value_from_window(ViewEditConfiguration.ID_END_TIME_UNITS),
            "is_fixed": self.gui.get_value_from_window(ViewEditConfiguration.ID_FIXED),
            "is_continuous": self.gui.get_value_from_window(ViewEditConfiguration.ID_CONTINUOUS),
            "total_samples": self.gui.get_value_from_window(ViewEditConfiguration.ID_TOTAL_SAMPLES)
        }

    def _check_values(self):
        self.fail_if(self._values is None, 'No values from the GUI available')
        # Check the values from the GUI to the configuration values
        # Sample time with sample time units
        sample_time = float(self._values["sample_time"])
        if self._values["sample_time_units"] == "days":
            sample_time *= 86400
        elif self._values["sample_time_units"] == "hours":
            sample_time *= 3600
        elif self._values["sample_time_units"] == "minutes":
            sample_time *= 60
        elif self._values["sample_time_units"] != "seconds":
            self.fail("The sample time units are not correct: '{}'".format(self._values["sample_time_units"]))
        self.fail_if(sample_time != self._conf.get_sample_time(),
                     "Sample time does not have the correct value, is {} expected {}".format(
                        sample_time, self._conf.get_sample_time()))
        # End time with end time units
        end_time = float(self._values["end_time"])
        if self._values["end_time_units"] == "days":
            end_time *= 86400
        elif self._values["end_time_units"] == "hours":
            end_time *= 3600
        elif self._values["end_time_units"] == "minutes":
            end_time *= 60
        elif self._values["end_time_units"] != "seconds":
            self.fail("The end time units are not correct: '{}'".format(self._values["end_time_units"]))
        self.fail_if(end_time != self._conf.get_end_time(),
                     "End time does not have the correct value, is {} expected {}".format(
                         end_time, self._conf.get_end_time()))
        # Continuous mode
        self.fail_if(self._values["is_continuous"] != self._conf.get_continuous_mode(),
                     "Continuous mode does not have the correct value, is {} expected {}".format(
                         self._values["is_continuous"], self._conf.get_continuous_mode()))
        # Fixed mode
        self.fail_if(self._values["is_fixed"] == self._conf.get_continuous_mode(),
                     "Fixed edn time mode does not have the correct value, is {} expected {}".format(
                         self._values["is_fixed"], not self._conf.get_continuous_mode()))
        # Total samples
        total_samples = int(end_time / sample_time) + 1
        self.fail_if(int(self._values["total_samples"]) != total_samples,
                     "Total samples does not have the correct value, is {} expected {}".format(
                         self._values["total_samples"], total_samples))

    def _get_default_values(self):
        self.log.debug("Get default values")
        self._values = None
        while True:
            if self.gui.is_window_available(ViewEditConfiguration.ID_SAMPLE_TIME):
                self._values = self._get_values_from_view()
                self.gui.click_button(wx.ID_CANCEL)
            self.sleep(0.1)

    def test_show_edit_configuration(self):
        self.start_thread(self._get_default_values)
        ControllerConfiguration.edit_configuration(self._conf, None, self.log)
        self._check_values()

    def teardown(self):
        self._app.MainLoop()


if __name__ == "__main__":

    TestControllerConfiguration().run(True)
