"""
Check for instrument on serial port.
"""

import serial
import time


def check_serial_port(port_name, baud_rate, command, response, rx_timeout=1):
    write_timeout = 0.2
    n_tries = 3
    while n_tries > 0:
        try:
            with serial.Serial(port_name, baudrate=baud_rate, write_timeout=write_timeout) as s:
                s.write(command)
                rx_data = b""
                t = rx_timeout
                while t > 0:
                    if s.in_waiting > 0:
                        rx_data += s.read(s.in_waiting)
                    if response in rx_data:
                        return True
                    time.sleep(0.1)
                    t -= 0.1
        except (Exception, ):
            pass
        n_tries -= 1

    return False


if __name__ == "__main__":

    print(check_serial_port("COM3", 115200, b"*IDN?\n", b"THURLBY THANDAR, PL303QMD-P"))
    print(check_serial_port("COM4", 115200, b"*IDN?\n", b"THURLBY THANDAR, PL303QMD-P"))
