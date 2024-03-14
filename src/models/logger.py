"""
Logger for the application.
"""

import os
import sys

from datetime import datetime
from src.app_data import AppData


class Logger:

    TYPE_INFO = "INFO"
    TYPE_DEBUG = "DEBUG"
    TYPE_ERROR = "ERROR"
    TYPE_STDOUT = "STDOUT"
    TYPE_STDERR = "STDERR"

    _TIME_STAMP_FORMAT = "%Y%m%d %H:%M:%S.%f"
    _LOG_FORMAT = "{} | {:6} | {}\n"

    _FILENAME = os.path.join(AppData.USER_FOLDER, f"{AppData.EXE_NAME}.log")

    class _StdLogger:

        def __init__(self, logger, std_type):
            self._logger = logger
            self._type = std_type

        def write(self, message):
            self._logger.handle_message(self._type, message)

        def flush(self):
            pass

    def __init__(self, log_to_stdout=False, redirect_stdout=True):
        self._log_to_stdout = log_to_stdout
        with open(self._FILENAME, "w", encoding="utf-8") as fp:
            fp.close()
        self._output = ""

        self._org_stdout = sys.stdout
        self._org_stderr = sys.stderr
        if redirect_stdout:
            sys.stdout = self._StdLogger(self, self.TYPE_STDOUT)
            sys.stderr = self._StdLogger(self, self.TYPE_STDERR)

    @classmethod
    def get_filename(cls):
        return cls._FILENAME

    def shut_down(self):
        sys.stdout = self._org_stdout
        sys.stderr = self._org_stderr

    def info(self, message):
        self.handle_message(self.TYPE_INFO, f"{message}\n")

    def debug(self, message):
        self.handle_message(self.TYPE_DEBUG, f"{message}\n")

    def error(self, message):
        self.handle_message(self.TYPE_ERROR, f"{message}\n")

    def handle_message(self, message_type, message_text):
        timestamp = datetime.now().strftime(self._TIME_STAMP_FORMAT)[:-3]
        self._output += message_text
        while "\n" in self._output:
            index = self._output.find("\n")
            message = self._LOG_FORMAT.format(timestamp, message_type, self._output[:index])
            self._output = self._output[index + 1:]
            with open(self._FILENAME, "a", encoding="utf-8") as fp:
                fp.write(message)
            if self._log_to_stdout:
                self._org_stdout.write(message)


if __name__ == "__main__":

    from tests.unit_tests.test_models.test_logger import TestLogger

    TestLogger().run()
