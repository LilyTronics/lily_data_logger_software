"""
Test for the settings model.
"""

import os

from src.models.settings import Settings
from tests.unit_tests.lib.test_suite import TestSuite


class TestSettings(TestSuite):

    def setup(self):
        self._settings = Settings()
        if os.path.isfile(self._settings._settings_file):
            os.remove(self._settings._settings_file)

    def test_main_window_size(self):
        self.fail_if(self._settings.get_main_window_size() != (-1, -1), "Default settings incorrect")
        self._settings.store_main_window_size(100, 100)
        self.fail_if(self._settings.get_main_window_size() != (100, 100), "Failed storing settings")

    def test_main_window_position(self):
        self.fail_if(self._settings.get_main_window_position() != (-1, -1), "Default settings incorrect")
        self._settings.store_main_window_position(10, 10)
        self.fail_if(self._settings.get_main_window_position() != (10, 10), "Failed storing settings")

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
        self.fail_if(self._settings.get_log_window_position() != (-1, -1), "Default settings incorrect")
        self._settings.store_log_window_position(20, 20)
        self.fail_if(self._settings.get_log_window_position() != (20, 20), "Failed storing settings")

    def test_log_window_maximized(self):
        self.fail_if(self._settings.get_log_window_maximized(), "Default settings incorrect")
        self._settings.store_log_window_maximized(True)
        self.fail_if(not self._settings.get_log_window_maximized(), "Failed storing settings")
        self._settings.store_log_window_maximized(False)


if __name__ == "__main__":

    TestSettings().run()
