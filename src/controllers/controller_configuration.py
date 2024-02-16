"""
Controller for handling the configuration.
"""

import wx

from src.views.view_dialogs import ViewDialogs
from src.views.view_edit_configuration import ViewEditConfiguration


class ControllerConfiguration:

    _FILE_FILTER = "Configuration files (*.json)|*.json"

    @classmethod
    def check_configuration_is_changed(cls, parent, configuration, logger):
        if configuration.is_changed():
            btn = ViewDialogs.show_confirm(parent,
                                           "The configuration is changed. Save configuration?",
                                           "Save configuration")
            if btn == wx.ID_YES:
                cls.save_to_file(parent, configuration, logger)
            wx.YieldIfNeeded()

    @classmethod
    def load_from_file(cls, parent, configuration, logger):
        dlg_title = "Open configuration"
        cls.check_configuration_is_changed(parent, configuration, logger)
        filename = ViewDialogs.show_open_file(parent, dlg_title, file_filter=cls._FILE_FILTER)
        if filename is not None:
            logger.debug(f"Load configuration from file: {filename}")
            try:
                configuration.load_from_file(filename)
            except Exception as e:
                logger.error(str(e))
                ViewDialogs.show_message(parent, f"Error when reading file {filename}:\n{e}",
                                         dlg_title)
        wx.YieldIfNeeded()

    @classmethod
    def save_to_file(cls, parent, configuration, logger):
        dlg_title = "Save configuration"
        filename = ViewDialogs.show_save_file(parent, dlg_title, file_filter=cls._FILE_FILTER)
        if filename is not None:
            logger.debug(f"Save configuration to file: {filename}")
            try:
                configuration.save_to_file(filename)
            except Exception as e:
                logger.error(str(e))
                ViewDialogs.show_message(parent, f"Error when writing file {filename}:\n{e}",
                                         dlg_title)
        wx.YieldIfNeeded()

    @staticmethod
    def edit_configuration(parent, configuration, logger):
        dlg = ViewEditConfiguration(parent)
        dlg.set_sample_time(configuration.get_sample_time())
        dlg.set_end_time(configuration.get_end_time())
        dlg.set_continuous_mode(configuration.get_continuous_mode())
        if dlg.ShowModal() == wx.ID_OK:
            logger.info("Edit configuration settings")
            current_sample_time = configuration.get_sample_time()
            new_sample_time = dlg.get_sample_time()
            if current_sample_time != new_sample_time:
                configuration.set_sample_time(new_sample_time)
                logger.debug(f"Sample time changed from {current_sample_time} to "
                             f"{new_sample_time} seconds")
            current_end_time = configuration.get_end_time()
            new_end_time = dlg.get_end_time()
            if current_end_time != new_end_time:
                configuration.set_end_time(new_end_time)
                logger.debug(f"End time changed from {current_end_time} to {new_end_time} seconds")
            current_continuous_mode = configuration.get_continuous_mode()
            new_continuous_mode = dlg.get_continuous_mode()
            if current_continuous_mode != new_continuous_mode:
                configuration.set_continuous_mode(new_continuous_mode)
                logger.debug(f"Continuous mode changed from {current_continuous_mode} "
                             f"to {new_continuous_mode}")
        dlg.Destroy()
        wx.YieldIfNeeded()


if __name__ == "__main__":

    import pylint
    from tests.unit_tests.test_controller_configuration import TestControllerConfiguration

    TestControllerConfiguration().run(True)
    pylint.run_pylint([__file__])
