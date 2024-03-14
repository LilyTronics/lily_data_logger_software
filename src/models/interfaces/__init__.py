"""
Interfaces package.
"""

from src.models.interfaces.serial_port_interface import SerialPortInterface
from src.models.interfaces.tcp_client_interface import TcpClientInterface
from src.models.interfaces.udp_client_interface import UdpClientInterface


class Interfaces:

    _INTERFACES = [
        SerialPortInterface,
        TcpClientInterface,
        UdpClientInterface
    ]

    @classmethod
    def get_interface_names(cls):
        return sorted(list(map(lambda x: x.NAME, cls._INTERFACES)))

    @classmethod
    def get_interface_by_name(cls, interface_name):
        matches = list(filter(lambda x: x.NAME == interface_name, cls._INTERFACES))
        if len(matches) == 1:
            return matches[0]
        return None


if __name__ == "__main__":

    from tests.unit_tests.test_models.test_interfaces import TestInterfaces

    TestInterfaces().run()
