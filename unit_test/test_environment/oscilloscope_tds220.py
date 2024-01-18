"""
Detect the oscilloscope TDS220.
- 9600 baud, flow control none, EOL LF
"""

import serial
import time


def get_oscilloscope_serial_port(serial_ports):
    id_command = b"*IDN?\n"
    id_data = b"TEKTRONIX,TDS 220"

    print("Checking all available ports for the TDS220")
    for port_name in serial_ports:
        print("Check for TDS220 on port: {}".format(port_name))
        n_tries = 3
        while n_tries > 0:
            try:
                with serial.Serial(port_name, 9600, write_timeout=0.2) as s:
                    s.write(id_command)
                    i = 5
                    rx_data = b""
                    while i > 0:
                        if s.in_waiting > 0:
                            rx_data += s.read(s.in_waiting)
                        if id_data in rx_data:
                            return port_name
                        time.sleep(0.1)
                        i -= 1
                    else:
                        raise Exception("RX timeout")
            except Exception as e:
                if n_tries == 1:
                    print("No oscilloscope: {}".format(e))
            n_tries -= 1

    return None


if __name__ == "__main__":

    from src.models.list_serial_ports import get_available_serial_ports

    print(get_oscilloscope_serial_port(get_available_serial_ports()))
