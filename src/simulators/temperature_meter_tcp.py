"""
Temperature meter using TCP interface.
"""

import random
import socket
import threading

from src.simulators.simulator_settings import SimulatorSettings


class TemperatureMeterTcp:

    _CMD_TEMPERATURE = b"T?"

    _RX_BUFFER_SIZE = 1500
    _TERMINATOR = b"\n"

    _TEMP_RANGE = (15, 25)

    def __init__(self):
        self._thread = None
        self._stop_event = threading.Event()

    def __del__(self):
        self.stop()

    ###########
    # Private #
    ###########

    def _handle_messages(self):
        sock = socket.create_server((SimulatorSettings.TemperatureMeterTcp.IP,
                                     SimulatorSettings.TemperatureMeterTcp.PORT))
        sock.settimeout(SimulatorSettings.TemperatureMeterTcp.RX_TIME_OUT)
        while not self._stop_event.is_set():
            try:
                connection = sock.accept()[0]
            except TimeoutError:
                continue

            data = connection.recv(self._RX_BUFFER_SIZE)
            response = "UNKNOWN COMMAND"

            if data.endswith(self._TERMINATOR):
                data = data[:-1]
                if data == self._CMD_TEMPERATURE:
                    response = f"T={random.uniform(*self._TEMP_RANGE):.1f}C"

            connection.sendall(response.encode("latin") + self._TERMINATOR)

        sock.close()

    ##########
    # Public #
    ##########

    def start(self):
        if self._thread is None or not self._thread.is_alive():
            self._stop_event.clear()
            self._thread = threading.Thread(target=self._handle_messages)
            self._thread.daemon = True
            self._thread.start()

    def stop(self):
        if self.is_running():
            self._stop_event.set()
            self._thread.join()

    def is_running(self):
        return self._thread is not None and self._thread.is_alive()


if __name__ == "__main__":

    import pylint
    from tests.unit_tests.test_models.test_simulator_temperature_meter import (
        TestSimulatorTemperatureMeter)

    TestSimulatorTemperatureMeter().run(True)
    pylint.run_pylint([__file__])
