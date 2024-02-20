"""
Test for the TCP client interface.
"""

import socket
import threading

from src.models.interfaces.tcp_client_interface import TcpClientInterface
from tests.unit_tests.lib.test_suite import TestSuite


class TestTcpClientInterface(TestSuite):

    _IP = "localhost"
    _PORT = 21000
    _CLIENT_TIMEOUT = 0.5
    _SERVER_TIMEOUT = 0.1
    _RX_BUFFER_SIZE = 1500
    _TEST_DATA = b"test TCP interface"
    _TEST_TIMEOUT_DATA = b"do_timeout"

    _socket = None
    _stop_event = None
    _thread = None
    _client = None

    def _start_server(self):
        def _process_data():
            while not self._stop_event.is_set():
                try:
                    connection = self._socket.accept()[0]
                except TimeoutError:
                    continue
                data = connection.recv(self._RX_BUFFER_SIZE)
                if data == self._TEST_TIMEOUT_DATA:
                    continue
                connection.sendall(data)

        self._socket = socket.create_server((self._IP, self._PORT))
        self._socket.settimeout(self._SERVER_TIMEOUT)
        self._stop_event = threading.Event()
        self._thread = self.start_thread(_process_data)

    def setup(self):
        self._client = TcpClientInterface(self._IP, self._PORT, self._CLIENT_TIMEOUT)

    def test_no_server_running(self):
        result = False
        try:
            self._client.send_command(self._TEST_DATA, True, b"", b"")
        except Exception as e:
            self.log.debug(f"Error message: {e}")
            if str(e).startswith("Could not connect to "):
                result = True
            else:
                self.log.error("Invalid error message, expect to start with: "
                               "'Could not connect to'")
        return result

    def test_server_running(self):
        self._start_server()
        response = self._client.send_command(self._TEST_DATA, True, b"", b"")
        self.log.debug(f"Response: {response}")
        self.fail_if(response != self._TEST_DATA,
                     f"Invalid response received, expected: '{self._TEST_DATA}'")

    def test_timeout(self):
        result = False
        try:
            self._client.send_command(self._TEST_TIMEOUT_DATA, True, b"", b"")
        except Exception as e:
            self.log.debug(f"Error message: {e}")
            if str(e) == "Error receiver timeout":
                result = True
            else:
                self.log.error("Invalid error message, expected: 'Error receiver timeout'")
        return result

    def teardown(self):
        if self._stop_event is not None:
            self._stop_event.set()
        if self._thread is not None:
            self._thread.join()
        if self._socket is not None:
            self._socket.close()
        if self._client is not None:
            self._client.close()


if __name__ == "__main__":

    import pylint

    TestTcpClientInterface().run(True)
    pylint.run_pylint([__file__])
