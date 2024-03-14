"""
Test for the settings model.
"""

import os

from src.models.settings import Settings
from tests.unit_tests.lib.test_suite import TestSuite


class TestSettings(TestSuite):

    _settings = None

    def setup(self):
        self._settings = Settings()
        if os.path.isfile(self._settings.get_filename()):
            os.remove(self._settings.get_filename())

    def test_main_window_size(self):
        self.fail_if(self._settings.get_main_window_size() != (-1, -1),
                     "Default settings incorrect")
        self._settings.store_main_window_size(100, 100)
        self.fail_if(self._settings.get_main_window_size() != (100, 100), "Failed storing settings")

    def test_main_window_position(self):
        self.fail_if(self._settings.get_main_window_position() != (-1, -1),
                     "Default settings incorrect")
        self._settings.store_main_window_position(10, 10)
        self.fail_if(self._settings.get_main_window_position() != (10, 10),
                     "Failed storing settings")

    def test_main_window_maximized(self):
        self.fail_if(self._settings.get_main_window_maximized(), "Default settings incorrect")
        self._settings.store_main_window_maximized(True)
        self.fail_if(not self._settings.get_main_window_maximized(), "Failed storing settings")
        self._settings.store_main_window_maximized(False)

    def test_log_window_size(self):
        self.fail_if(self._settings.get_log_window_size() != (-1, -1), "Default settings incorrect")
        self._settings.store_log_window_size(200, 200)
        self.fail_if(self._settings.get_log_window_size() != (200, 200), "Failed storing settings")

    def test_log_window_position(self):
        self.fail_if(self._settings.get_log_window_position() != (-1, -1),
                     "Default settings incorrect")
        self._settings.store_log_window_position(20, 20)
        self.fail_if(self._settings.get_log_window_position() != (20, 20),
                     "Failed storing settings")

    def test_log_window_maximized(self):
        self.fail_if(self._settings.get_log_window_maximized(), "Default settings incorrect")
        self._settings.store_log_window_maximized(True)
        self.fail_if(not self._settings.get_log_window_maximized(), "Failed storing settings")
        self._settings.store_log_window_maximized(False)

    def test_recent_configurations(self):
        self.fail_if(len(self._settings.get_recent_configurations()) > 0,
                     "Default settings incorrect")
        for i in range(15):
            filename = f"config_file_{i}.json"
            self._settings.add_to_recent_configurations(filename)
            configs = self._settings.get_recent_configurations()
            self.fail_if(configs[0] != filename, "Filename is not added properly")
            self.fail_if(len(configs) > 10, "Too many filenames in the list")

    def test_move_to_top(self):
        configs = self._settings.get_recent_configurations()
        filename = configs[3]
        self._settings.add_to_recent_configurations(filename)
        configs = self._settings.get_recent_configurations()
        self.fail_if(configs[0] != filename, "The filename is not at the top")
        self.fail_if(filename in configs[1:], "The filename is two times in the list")

    def test_remove_configuration(self):
        configs = self._settings.get_recent_configurations()
        filename = configs[3]
        self._settings.remove_recent_configuration(filename)
        configs = self._settings.get_recent_configurations()
        self.fail_if(filename in configs, "Filename was not removed")


if __name__ == "__main__":

    TestSettings().run(True)
