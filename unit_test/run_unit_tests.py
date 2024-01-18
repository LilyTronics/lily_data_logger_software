"""
Runs all the unit tests
"""

import os

from lily_unit_test import TestRunner
from src.models.list_serial_ports import get_available_serial_ports
from unit_test.test_environment.power_supply_pl303qmd import get_power_supply_serial_port
from unit_test.test_environment.serial_loopback import get_serial_loopback_port
from unit_test.test_environment.setup_environment import clear_reports


REPORT_FOLDER = os.path.join(os.path.dirname(__file__), "test_reports")
EXCLUDE_TESTS = ["TestSuite"]
serial_ports = get_available_serial_ports()

clear_reports(REPORT_FOLDER)

if get_serial_loopback_port(serial_ports) is None:
    EXCLUDE_TESTS.append("TestSerialPortInterface")

if get_power_supply_serial_port(serial_ports) is None:
    EXCLUDE_TESTS.append("TestPowerSupplyPL303QMD")

options = {
    "report_folder": REPORT_FOLDER,
    "create_html_report": True,
    "open_in_browser": True,
    "no_log_files": True,
    "exclude_test_suites": EXCLUDE_TESTS
}
TestRunner.run("../src", options)
