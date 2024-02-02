"""
Script that runs before all tests to set up the environment
"""

import os
import shutil

from src.models.list_serial_ports import get_available_serial_ports
from tests.test_environment.check_arduino_uno_daq import get_arduino_uno_daq_serial_port
from tests.test_environment.check_serial_loopback import get_serial_loopback_port


def clear_reports(report_path):
    print("Clear report path: {}".format(report_path))
    for item in os.listdir(report_path):
        full_path = os.path.join(report_path, item)
        if os.path.isfile(full_path):
            os.remove(full_path)
        elif os.path.isdir(full_path):
            shutil.rmtree(full_path)
        else:
            raise Exception("ERROR: could not remove item '{}'".format(item))


def check_for_instruments():
    exclude_tests = []

    print("Detect available serial ports")
    serial_ports = get_available_serial_ports()
    print("Available ports: {}".format(serial_ports))

    if get_serial_loopback_port(serial_ports) is None:
        exclude_tests.append("TestSerialPortInterface")

    if get_arduino_uno_daq_serial_port(serial_ports) is None:
        exclude_tests.append("TestArduinoUnoDAQ")

    return exclude_tests


if __name__ == "__main__":

    clear_reports("..\\test_reports")
    print("Exclude:", check_for_instruments())
