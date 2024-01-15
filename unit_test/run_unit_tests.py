"""
Runs all the unit tests
"""

import os

from lily_unit_test import TestRunner
from unit_test.setup_environment import setup_environment


REPORT_FOLDER = os.path.join(os.path.dirname(__file__), 'test_reports')
EXCLUDE_TESTS = ['TestSuite']

setup_environment(REPORT_FOLDER, EXCLUDE_TESTS)

options = {
    'report_folder': REPORT_FOLDER,
    'create_html_report': True,
    'open_in_browser': True,
    'no_log_files': True,
    'exclude_test_suites': EXCLUDE_TESTS
}
TestRunner.run('../src', options)
