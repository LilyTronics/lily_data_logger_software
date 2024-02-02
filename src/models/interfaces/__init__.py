"""
Interfaces package.
"""

from src.models.interfaces.serial_port_interface import SerialPortInterface
from src.models.interfaces.tcp_client_interface import TcpClientInterface
from src.models.interfaces.udp_client_interface import UdpClientInterface
from tests.test_suite import TestSuite


_INTERFACES = [
    SerialPortInterface,
    TcpClientInterface,
    UdpClientInterface
]


def get_interface_names():
    return sorted(list(map(lambda x: x.NAME, _INTERFACES)))


def get_interface_by_name(interface_name):
    matches = list(filter(lambda x: x.NAME == interface_name, _INTERFACES))
    if len(matches) == 1:
        return matches[0]
    return None


class TestInterfaces(TestSuite):

    def test_interfaces(self):
        for name in get_interface_names():
            self.log.debug("{:12}: {}".format(name, get_interface_by_name(name)))
        interface = get_interface_by_name("Unknown interface name")
        self.fail_if(interface is not None, "Unknown interface name did not return None")


if __name__ == "__main__":

    TestInterfaces().run()
