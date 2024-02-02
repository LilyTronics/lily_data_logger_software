"""
UDP client interface.
"""

import socket

from src.models.interfaces.interface import Interface


class UdpClientInterface(Interface):

    NAME = "Ethernet UDP"

    def __init__(self, server_ip_address, server_port, timeout, rx_buffer_size=1500):
        self._server_ip_address = server_ip_address
        self._server_port = server_port
        self._rx_buffer_size = rx_buffer_size
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._socket.settimeout(timeout)

    def send_command(self, command):
        response = b""
        self._socket.sendto(command, (self._server_ip_address, self._server_port))
        try:
            response = self._socket.recv(self._rx_buffer_size)
        except ConnectionResetError:
            self.raise_connection_exception(f"{self._server_ip_address}:{self._server_port}")
        except TimeoutError:
            self.raise_timeout_exception()

        return response

    def close(self):
        self._socket.close()


if __name__ == "__main__":

    from tests.unit_tests.test_udp_client_interface import TestUdpClientInterface

    TestUdpClientInterface().run()
