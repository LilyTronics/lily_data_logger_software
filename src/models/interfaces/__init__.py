"""
Interfaces package.
"""

from src.models.interfaces.serial_port_interface import SerialPortInterface
from src.models.interfaces.tcp_client_interface import TcpClientInterface
from src.models.interfaces.udp_client_interface import UdpClientInterface


_INTERFACES = [
    SerialPortInterface,
    TcpClientInterface,
    UdpClientInterface
]


def get_interface_names():
    return sorted(list(map(lambda x: x.NAME, _INTERFACES)))


def get_interface_by_name(interface_name):
    matches = list(filter(lambda x: x.NAME == interface_name, _INTERFACES))
    assert len(matches) == 1, 'Interface with name {} not found'.format(interface_name)
    return matches[0]


if __name__ == '__main__':

    for name in get_interface_names():
        print('{:12}: {}'.format(name, get_interface_by_name(name)))
