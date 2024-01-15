"""
Script that runs before all tests to set up the environment
"""

import os
import serial
import shutil
import time

from src.models.list_serial_ports import get_available_serial_ports


def setup_environment(report_path, exclude_tests):
    _clear_reports(report_path)
    if not _serial_port_loopback_is_available():
        exclude_tests.append('TestSerialPortInterface')


def _clear_reports(report_path):
    print('Clear report path {}'.format(report_path))
    for item in os.listdir(report_path):
        full_path = os.path.join(report_path, item)
        if os.path.isfile(full_path):
            os.remove(full_path)
        elif os.path.isdir(full_path):
            shutil.rmtree(full_path)
        else:
            raise Exception('ERROR: could not remove item: {}'.format(item))


def _serial_port_loopback_is_available():
    loopback_found = False

    _CHECK_FOR_LOOPBACK_DATA = b'check_for_loopback'
    _TEST_COMMAND = b'serial_port_test'
    _RX_TIMEOUT = 1

    print('Checking all available ports for a loopback')
    for port_name in get_available_serial_ports():
        print('Check for loopback on port: {}'.format(port_name))
        with serial.Serial(port_name, write_timeout=0.2) as s:
            try:
                s.write(_CHECK_FOR_LOOPBACK_DATA)
            except serial.serialutil.SerialTimeoutException:
                print('Could not write data to port')
                continue

            i = 5
            rx_data = b''
            while i > 0:
                if s.in_waiting > 0:
                    rx_data += s.read(s.in_waiting)
                if rx_data == _CHECK_FOR_LOOPBACK_DATA:
                    loopback_found = True
                    break
                time.sleep(0.1)
                i -= 1
            else:
                print('Loopback data not found (timeout)')

    return loopback_found


if __name__ == '__main__':

    tests_to_exclude = []
    setup_environment('test_reports', tests_to_exclude)
    print(tests_to_exclude)
