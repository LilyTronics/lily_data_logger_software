"""
Runs all the unit tests
"""

import os

from lily_unit_test import TestRunner
from src.models.list_serial_ports import get_available_serial_ports
from unit_test.test_environment.check_serial_loopback import is_serial_loopback_available
from unit_test.test_environment.setup_environment import clear_reports


REPORT_FOLDER = os.path.join(os.path.dirname(__file__), 'test_reports')
EXCLUDE_TESTS = ['TestSuite']
serial_ports = get_available_serial_ports()

clear_reports(REPORT_FOLDER)

if not is_serial_loopback_available(serial_ports):
    EXCLUDE_TESTS.append('TestSerialPortInterface')

options = {
    'report_folder': REPORT_FOLDER,
    'create_html_report': True,
    'open_in_browser': True,
    'no_log_files': True,
    'exclude_test_suites': EXCLUDE_TESTS
}
TestRunner.run('../src', options)
