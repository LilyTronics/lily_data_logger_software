"""
UDP client interface.
"""

import socket
import threading

from src.models.interfaces.udp_client_interface import UdpClientInterface
from tests.unit_tests.lib.test_suite import TestSuite


class TestUdpClientInterface(TestSuite):

    _IP = "localhost"
    _PORT = 20000
    _CLIENT_TIMEOUT = 0.5
    _SERVER_TIMEOUT = 0.1
    _RX_BUFFER_SIZE = 1500
    _TEST_DATA = b"test UDP interface"
    _TEST_TIMEOUT_DATA = b"do_timeout"

    _socket = None
    _stop_event = None
    _thread = None

    def _start_server(self):
        def _process_data():
            while not self._stop_event.is_set():
                try:
                    data, client_address = self._socket.recvfrom(self._RX_BUFFER_SIZE)
                    if data == self._TEST_TIMEOUT_DATA:
                        continue
                    self._socket.sendto(data, client_address)
                except TimeoutError:
                    pass

        self._socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._socket.settimeout(self._SERVER_TIMEOUT)
        self._socket.bind((self._IP, self._PORT))
        self._stop_event = threading.Event()
        self._thread = self.start_thread(_process_data)

    def setup(self):
        self._client = UdpClientInterface(self._IP, self._PORT, self._CLIENT_TIMEOUT)

    def test_no_server_running(self):
        result = False
        try:
            self._client.send_command(self._TEST_DATA, True, b"", b"")
        except Exception as e:
            self.log.debug("Error message: {}".format(e))
            if str(e).startswith("Could not connect to "):
                result = True
            else:
                self.log.error("Invalid error message, expect to start with: 'Could not connect to'")
        return result

    def test_server_running(self):
        self._start_server()
        response = self._client.send_command(self._TEST_DATA, True, b"", b"")
        self.log.debug("Response: {}".format(response))
        self.fail_if(response != self._TEST_DATA, "Invalid response received, expected: '{}'".format(self._TEST_DATA))

    def test_timeout(self):
        result = False
        try:
            self._client.send_command(self._TEST_TIMEOUT_DATA, True, b"", b"")
        except Exception as e:
            self.log.debug("Error message: {}".format(e))
            if str(e) == "Error receiver timeout":
                result = True
            else:
                self.log.error("Invalid error message, expected: 'Error receiver timeout'")
        return result

    def teardown(self):
        if None not in (self._socket, self._stop_event, self._thread):
            self._stop_event.set()
            self._thread.join()
            self._socket.close()
        self._client.close()


if __name__ == "__main__":

    TestUdpClientInterface().run()
