"""
Test configurations containing various test configurations.
"""

import os
import shutil

from src.app_data import AppData
from src.models.configuration import Configuration


class TestConfigurations:

    _CONFIGURATIONS = {}

    _REQUIRED_USER_FILES = [
        "instrument_delayed_measurement.json"
    ]

    ##########
    # Public #
    ##########

    @classmethod
    def init(cls):
        cls._copy_user_files()
        cls._CONFIGURATIONS["all simulators, 2s/7s"] = "config_all_simulators_2_7.json"
        cls._CONFIGURATIONS["failing measurement"] = "config_failing_measurement.json"
        cls._CONFIGURATIONS["delayed measurement"] = "configuration_delayed_measurement.json"

    @classmethod
    def get_configuration_names(cls):
        return list(cls._CONFIGURATIONS)

    @classmethod
    def get_configuration(cls, name):
        config = Configuration()
        filename = cls._CONFIGURATIONS.get(name)
        if filename is not None:
            full_path = os.path.join(os.path.dirname(__file__), "test_files", filename)
            config.load_from_file(full_path)
        return config

    @classmethod
    def get_unit_test_configuration(cls):
        return cls.get_configuration("all simulators, 2s/7s")

    ###########
    # Private #
    ###########

    @classmethod
    def _copy_user_files(cls):
        for filename in cls._REQUIRED_USER_FILES:
            source = os.path.join(os.path.dirname(__file__), "test_files", filename)
            destination = os.path.join(AppData.USER_FOLDER, filename)
            shutil.copy(str(source), str(destination))



# Initialize the test configurations
TestConfigurations.init()


if __name__ == "__main__":

    for _name in TestConfigurations.get_configuration_names():
        print(_name, TestConfigurations.get_configuration(_name).__class__)
