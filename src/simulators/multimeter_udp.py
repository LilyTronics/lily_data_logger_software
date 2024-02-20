"""
Multimeter using UDP interface.
"""

import random
import socket
import threading

from src.simulators.simulator_settings import SimulatorSettings


class MultimeterUdp:

    _CMD_VOLTAGE_DC = b"VDC?"
    _CMD_CURRENT_DC = b"ADC?"

    _RX_BUFFER_SIZE = 1500
    _TERMINATOR = b"\n"

    _VDC_RANGE = (4.9, 5.1)
    _ADC_RANGE = (0.39, 0.41)

    def __init__(self):
        self._thread = None
        self._stop_event = threading.Event()

    def __del__(self):
        self.stop()

    ###########
    # Private #
    ###########

    def _handle_messages(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.settimeout(SimulatorSettings.MultimeterUdp.RX_TIME_OUT)
        sock.bind((SimulatorSettings.MultimeterUdp.IP, SimulatorSettings.MultimeterUdp.PORT))
        while not self._stop_event.is_set():
            try:
                response = "UNKNOWN COMMAND"
                data, client_address = sock.recvfrom(self._RX_BUFFER_SIZE)
                if data.endswith(self._TERMINATOR):
                    data = data[:-1]
                    if data == self._CMD_VOLTAGE_DC == data:
                        response = f"VDC={random.uniform(*self._VDC_RANGE):.3f}V"
                    elif data == self._CMD_CURRENT_DC:
                        response = f"ADC={random.uniform(*self._ADC_RANGE):.3f}A"
                sock.sendto(response.encode() + self._TERMINATOR, client_address)
            except TimeoutError:
                pass
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
    from tests.unit_tests.test_models.test_multimeter_udp import TestMultimeterUdp

    TestMultimeterUdp().run(True)
    pylint.run_pylint([__file__])
