"""
Check for instrument on serial port.
"""

import time
import serial


def check_serial_port(port_name, baud_rate, command, response, rx_timeout=1, toggle_dtr=False):
    write_timeout = 0.2
    with serial.Serial(port_name, baudrate=baud_rate, write_timeout=write_timeout) as s:
        if toggle_dtr:
            for state in (True, False, True):
                s.dtr = state
                time.sleep(0.005)
        n_tries = 3
        while n_tries > 0:
            try:
                s.write(command)
                rx_data = b""
                t = rx_timeout
                while t > 0:
                    if s.in_waiting > 0:
                        rx_data += s.read(s.in_waiting)
                    if isinstance(response, (list, tuple)):
                        for value in response:
                            if value in rx_data:
                                return True
                    elif response in rx_data:
                        return True
                    time.sleep(0.1)
                    t -= 0.1
            except (Exception, ):
                pass
            n_tries -= 1

    return False


if __name__ == "__main__":

    print(check_serial_port("COM9", 115200, b"rd2\n", b"\n", rx_timeout=2, toggle_dtr=True))
    print(check_serial_port("COM9", 115200, b"rd2\n", [b"0\n", b"1\n"], rx_timeout=2,
                            toggle_dtr=True))
    print(check_serial_port("COM9", 115200, b"rd2\n", (b"0\n", b"1\n"), rx_timeout=2,
                            toggle_dtr=True))
