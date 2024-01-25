"""
Detect the oscilloscope TDS220.
- 9600 baud, flow control none, EOL LF
"""

from unit_test.test_environment.check_serial_port import check_serial_port


def get_tds220_serial_port(serial_ports):
    print("Checking available ports for the TDS220")
    for port_name in serial_ports:
        print("Check for TDS220 on port: {}".format(port_name))
        if check_serial_port(port_name, 9600, b"*IDN?\n", b"TEKTRONIX,TDS 220"):
            print("TDS220 found on {}".format(port_name))
            return port_name
        print("TDS220 not found")
    print("No TDS220 found on any of the available ports")
    return None


if __name__ == "__main__":

    from src.models.list_serial_ports import get_available_serial_ports

    print(get_tds220_serial_port(get_available_serial_ports()))
