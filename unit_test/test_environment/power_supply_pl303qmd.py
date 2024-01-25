"""
Detect the power supply PL303QMD.
"""

from unit_test.test_environment.check_serial_port import check_serial_port


def get_pl303qmd_serial_port(serial_ports):
    print("Checking available ports for the PL303QMD")
    for port_name in serial_ports:
        print("Check for PL303QMD on port: {}".format(port_name))
        if check_serial_port(port_name, 9600, b"*IDN?\n", b"THURLBY THANDAR, PL303QMD-P"):
            print("PL303QMD found on {}".format(port_name))
            return port_name
        print("PL303QMD not found")
    print("No PL303QMD found on any of the available ports")
    return None


if __name__ == "__main__":

    from src.models.list_serial_ports import get_available_serial_ports

    print("\nPort:", get_pl303qmd_serial_port(get_available_serial_ports()))
