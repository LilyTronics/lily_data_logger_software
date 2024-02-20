"""
Runs the unit tests for the instruments.
This requires connected hardware.
"""

import os


from lily_unit_test import TestRunner
from tests.test_environment.setup_environment import clear_reports


REPORT_FOLDER = os.path.join(os.path.dirname(__file__), "test_reports")
EXCLUDE_TESTS = ["TestSuite", "TestControllerMain"]

if not os.path.isdir(REPORT_FOLDER):
    os.makedirs(REPORT_FOLDER)

clear_reports(REPORT_FOLDER)

options = {
    "report_folder": REPORT_FOLDER,
    "create_html_report": True,
    "open_in_browser": True,
    "no_log_files": True,
    "exclude_test_suites": EXCLUDE_TESTS
}
TestRunner.run("./unit_tests/test_models", options)
