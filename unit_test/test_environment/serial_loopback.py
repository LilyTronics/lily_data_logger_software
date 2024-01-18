"""
Check if a loopback is available on a serial port.
"""

import serial
import time


def get_serial_loopback_port(serial_ports):
    _CHECK_FOR_LOOPBACK_DATA = b"check_for_loopback"
    _RX_TIMEOUT = 1
    print("Checking all available ports for a loopback")
    for port_name in serial_ports:
        print("Check for loopback on port: {}".format(port_name))
        try:
            with serial.Serial(port_name, write_timeout=0.2) as s:
                s.write(_CHECK_FOR_LOOPBACK_DATA)
                i = 5
                rx_data = b""
                while i > 0:
                    if s.in_waiting > 0:
                        rx_data += s.read(s.in_waiting)
                    if rx_data == _CHECK_FOR_LOOPBACK_DATA:
                        return port_name
                    time.sleep(0.1)
                    i -= 1
                else:
                    raise Exception("RX timeout")
        except Exception as e:
            print("No loopback: {}".format(e))
    return None


if __name__ == "__main__":

    from src.models.list_serial_ports import get_available_serial_ports

    print(get_serial_loopback_port(get_available_serial_ports()))
