"""
Check if a loopback is available on a serial port.
"""

import serial
import time


def is_serial_loopback_available(serial_ports):
    loopback_found = False
    _CHECK_FOR_LOOPBACK_DATA = b'check_for_loopback'
    _TEST_COMMAND = b'serial_port_test'
    _RX_TIMEOUT = 1
    print('Checking all available ports for a loopback')
    for port_name in serial_ports:
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

    from src.models.list_serial_ports import get_available_serial_ports

    print(is_serial_loopback_available(get_available_serial_ports()))
