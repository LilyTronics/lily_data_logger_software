"""
Model for storing and recalling the application settings.
"""

import json
import os

from src.app_data import AppData


class Settings:

    def __init__(self):
        self._filename = os.path.join(AppData.USER_FOLDER,  f"{AppData.EXE_NAME}.json")

    ###########
    # Private #
    ###########

    def _read_settings(self):
        d = {}
        try:
            with open(self._filename, "r", encoding="utf-8") as fp:
                d = json.load(fp)
        except FileNotFoundError:
            pass
        except json.decoder.JSONDecodeError:
            pass

        return d

    def _write_settings(self, settings):
        with open(self._filename, "w", encoding="utf-8") as fp:
            json.dump(settings, fp, indent=2)

    def _get_property(self, main_key, sub_key, default=None):
        d = self._read_settings()
        return d.get(main_key, {}).get(sub_key, default)

    def _store_property(self, main_key, sub_key, value):
        d = self._read_settings()
        if main_key not in d.keys():
            d[main_key] = {}
        d[main_key][sub_key] = value
        self._write_settings(d)

    ##########
    # Public #
    ##########

    def get_filename(self):
        return self._filename

    ########################
    # Main window settings #
    ########################

    def get_main_window_size(self):
        return (self._get_property("main_window", "width", -1),
                self._get_property("main_window", "height", -1))

    def store_main_window_size(self, width, height):
        self._store_property("main_window", "width", width)
        self._store_property("main_window", "height", height)

    def get_main_window_position(self):
        return (self._get_property("main_window", "left", -1),
                self._get_property("main_window", "top", -1))

    def store_main_window_position(self, left, top):
        self._store_property("main_window", "left", left)
        self._store_property("main_window", "top", top)

    def get_main_window_maximized(self):
        return self._get_property("main_window", "maximized", False)

    def store_main_window_maximized(self, is_maximized):
        self._store_property("main_window", "maximized", is_maximized)

    #######################
    # Log window settings #
    #######################

    def get_log_window_size(self):
        return (self._get_property("log_window", "width", -1),
                self._get_property("log_window", "height", -1))

    def store_log_window_size(self, width, height):
        self._store_property("log_window", "width", width)
        self._store_property("log_window", "height", height)

    def get_log_window_position(self):
        return (self._get_property("log_window", "left", -1),
                self._get_property("log_window", "top", -1))

    def store_log_window_position(self, left, top):
        self._store_property("log_window", "left", left)
        self._store_property("log_window", "top", top)

    def get_log_window_maximized(self):
        return self._get_property("log_window", "maximized", False)

    def store_log_window_maximized(self, is_maximized):
        self._store_property("log_window", "maximized", is_maximized)


if __name__ == "__main__":

    import pylint
    from tests.unit_tests.test_models.test_settings import TestSettings

    TestSettings().run(True)
    pylint.run_pylint([__file__])
