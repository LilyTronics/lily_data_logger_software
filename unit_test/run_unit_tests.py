"""
Runs all the unit tests
"""

import os

from lily_unit_test import TestRunner
from unit_test.test_environment.setup_environment import clear_reports
from unit_test.test_environment.setup_environment import check_for_instruments


REPORT_FOLDER = os.path.join(os.path.dirname(__file__), "test_reports")
EXCLUDE_TESTS = ["TestSuite"]
EXCLUDE_TESTS.extend(check_for_instruments())

clear_reports(REPORT_FOLDER)

options = {
    "report_folder": REPORT_FOLDER,
    "create_html_report": True,
    "open_in_browser": True,
    "no_log_files": True,
    "exclude_test_suites": EXCLUDE_TESTS
}
TestRunner.run("../src", options)
