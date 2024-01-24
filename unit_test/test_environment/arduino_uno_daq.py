"""
Detect the Arduino Uno DAQ.
- 15200 baud, flow control none, EOL LF
"""

import serial
import time


def get_arduino_uno_daq_serial_port(serial_ports):
    print("Checking all available ports for the Arduino Uno DAQ")
    for port_name in serial_ports:
        print("Check for Arduino Uno DAQ on port: {}".format(port_name))
        try:
            with serial.Serial(port_name, 115200, write_timeout=0.2) as s:
                # Reset Arduino, toggle reset line by toggling the DRT.
                s.dtr = True
                time.sleep(0.01)
                s.dtr = False
                time.sleep(0.01)
                s.dtr = True
                n_tries = 3
                while n_tries > 0:
                    s.write(b"rd2\n")
                    i = 5
                    rx_data = b""
                    while i > 0:
                        if s.in_waiting > 0:
                            rx_data += s.read(s.in_waiting)
                        if b'\n' in rx_data and len(rx_data) == 2 and rx_data[0] in [48, 49]:
                            return port_name
                        time.sleep(0.1)
                        i -= 1
                    n_tries -= 1
        except (Exception, ):
            pass

    print("No Arduino Uno DAQ found")
    return None


if __name__ == "__main__":

    from src.models.list_serial_ports import get_available_serial_ports

    print(get_arduino_uno_daq_serial_port(get_available_serial_ports()))
