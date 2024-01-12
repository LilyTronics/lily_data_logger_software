"""
Controller for handling the configuration.
"""

import wx

from src.views.view_dialogs import show_confirm
from src.views.view_dialogs import show_message
from src.views.view_dialogs import show_open_file
from src.views.view_dialogs import show_save_file


class ControllerConfiguration(object):

    _FILE_FILTER = 'Configuration files (*.json)|*.json'

    @classmethod
    def check_configuration_is_changed(cls, configuration, parent_view, logger):
        if configuration.is_changed():
            btn = show_confirm(parent_view, 'The configuration is changed. Save configuration?', 'Save configuration')
            if btn == wx.ID_YES:
                cls.save_to_file(configuration, parent_view, logger)

    @classmethod
    def load_from_file(cls, configuration, parent_view, logger):
        dlg_title = 'Open configuration'
        cls.check_configuration_is_changed(configuration, parent_view, logger)
        filename = show_open_file(parent_view, dlg_title, file_filter=cls._FILE_FILTER)
        if filename is not None:
            logger.debug("Load configuration from file: '%s'" % filename)
            try:
                configuration.load_from_file(filename)
            except Exception as e:
                logger.error(str(e))
                show_message(parent_view, "Error when reading file '%s':\n'%s'" % (filename, e), dlg_title)

    @classmethod
    def save_to_file(cls, configuration, parent_view, logger):
        dlg_title = 'Save configuration'
        filename = show_save_file(parent_view, dlg_title, file_filter=cls._FILE_FILTER)
        if filename is not None:
            logger.debug("Save configuration to file: '%s'" % filename)
            try:
                configuration.save_to_file(filename)
            except Exception as e:
                logger.error(str(e))
                show_message(parent_view, "Error when writing file '%s':\n'%s'" % (filename, e), dlg_title)


if __name__ == '__main__':

    from src.models.configuration import Configuration
    from src.models.logger import Logger

    app = wx.App(redirect=False)

    test_logger = Logger(True)
    test_conf = Configuration()
    test_conf.set_end_time(120)

    ControllerConfiguration.check_configuration_is_changed(test_conf, None, test_logger)
    ControllerConfiguration.load_from_file(test_conf, None, test_logger)

    app.MainLoop()
