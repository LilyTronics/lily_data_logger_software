"""
Check if a loopback is available on a serial port.
"""

from tests.test_environment.check_serial_port import check_serial_port


def get_serial_loopback_port(serial_ports):
    print("Checking available ports for a loopback")
    for port_name in serial_ports:
        print(f"Check for loopback on port: {port_name}")
        if check_serial_port(port_name, 115200, b"CHECK_FOR_LOOPBACK", b"CHECK_FOR_LOOPBACK"):
            print(f"Loopback found on {port_name}")
            return port_name
        print("Loopback not found")
    print("No loopback found on any of the available ports")
    return None


if __name__ == "__main__":

    from src.models.list_serial_ports import get_available_serial_ports

    print(get_serial_loopback_port(get_available_serial_ports()))
