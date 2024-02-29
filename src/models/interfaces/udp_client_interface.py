"""
UDP client interface.
"""

import socket
import wx

from src.models.interfaces.interface import Interface


class UdpClientInterface(Interface):

    NAME = "Ethernet UDP"
    DEFAULT_TIMEOUT = 3

    def __init__(self, ip_address, ip_port, rx_timeout=DEFAULT_TIMEOUT, rx_buffer_size=1500):
        params_to_match = {
            "ip_address": ip_address,
            "ip_port": ip_port
        }
        super().__init__(params_to_match)
        self._server_ip_address = ip_address
        self._server_port = int(ip_port)
        self._rx_buffer_size = rx_buffer_size
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._socket.settimeout(float(rx_timeout))

    def is_open(self):
        return True

    def open(self):
        pass

    def send_command(self, command, expect_response, pre_response, post_response):
        response = b""
        self._socket.sendto(command, (self._server_ip_address, self._server_port))
        if expect_response:
            try:
                response = self._socket.recv(self._rx_buffer_size)
            except ConnectionResetError:
                self.raise_connection_exception(f"{self._server_ip_address}:{self._server_port}")
            except TimeoutError:
                self.raise_timeout_exception()

        return response

    def close(self):
        self._socket.close()

    @classmethod
    def get_settings_controls(cls):
        return {
            "ip_address": {
                "label": "IP Address",
                "control": wx.TextCtrl,
                "default": ""
            },
            "ip_port": {
                "label": "Port",
                "control": wx.TextCtrl,
                "default": ""
            },
            "rx_timeout": {
                "label": "RX timeout",
                "control": wx.TextCtrl,
                "default": ""
            }
        }


if __name__ == "__main__":

    import pylint
    from tests.unit_tests.test_models.test_udp_client_interface import TestUdpClientInterface

    TestUdpClientInterface().run(True)
    pylint.run_pylint([__file__])
