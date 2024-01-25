"""
Detect the Arduino Uno DAQ.
- 15200 baud, flow control none, EOL LF
"""

from unit_test.test_environment.check_serial_port import check_serial_port


def get_arduino_uno_daq_serial_port(serial_ports):
    print("Checking available ports for Arduino Uno DAQ")
    for port_name in serial_ports:
        print("Check for Arduino Uno DAQ on port: {}".format(port_name))
        if check_serial_port(port_name, 115200, b"rd2", [b"0\n", b"1\n"], rx_timeout=2, toggle_dtr=True):
            print("Arduino Uno DAQ found on {}".format(port_name))
            return port_name
        print("Arduino Uno DAQ not found")
    print("No Arduino Uno DAQ found on any of the available ports")
    return None


if __name__ == "__main__":

    from src.models.list_serial_ports import get_available_serial_ports

    print(get_arduino_uno_daq_serial_port(get_available_serial_ports()))
