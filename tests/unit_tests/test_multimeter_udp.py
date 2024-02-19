"""
Test multimeter using UDP interface.
"""

import socket
import threading

from src.simulators.multimeter_udp import MultimeterUdp
from src.simulators.simulator_settings import SimulatorSettings
from tests.unit_tests.lib.test_suite import TestSuite


class TestMultimeterUdp(TestSuite):

    _RX_TIME_OUT = 0.5
    _RX_BUFFER_SIZE = 1500
    _N_SAMPLES = 10
    _TERMINATOR = b"\n"

    _socket = None
    _multimeter = None
    _n_threads = 0

    def _log_running_threads(self):
        threads = ", ".join(map(str, threading.enumerate()))
        self.log.debug(f"Running threads: {threads}")

    def _send_command(self, command):
        self._socket.sendto(command + self._TERMINATOR,
                            (SimulatorSettings.MultimeterUdp.IP,
                             SimulatorSettings.MultimeterUdp.PORT))
        return self._socket.recv(self._RX_BUFFER_SIZE)

    def setup(self):
        self._n_threads = len(threading.enumerate())
        self._multimeter = MultimeterUdp()
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._socket.settimeout(self._RX_TIME_OUT)

    def test_start_stop(self):
        self.log.debug("Start multimeter")
        self._multimeter.start()
        self._log_running_threads()
        self.fail_if(len(threading.enumerate()) != self._n_threads + 1,
                     "The multimeter did not start properly")
        self.fail_if(not self._multimeter.is_running(), "The multimeter thread is not running")

        self.log.debug("Start multimeter while running")
        self._multimeter.start()
        self.fail_if(len(threading.enumerate()) != self._n_threads + 1,
                     "The multimeter did not ignore start while running")
        self.fail_if(not self._multimeter.is_running(),
                     "The multimeter thread is not running after start while running")

        self.log.debug("Stop multimeter")
        self._multimeter.stop()
        self.fail_if(len(threading.enumerate()) != self._n_threads, "The multimeter did not stop")
        self.fail_if(self._multimeter.is_running(),
                     "The multimeter thread is still running after stop")

        self.log.debug("Stop multimeter while not running")
        self._multimeter.stop()

        self.log.debug("Restart multimeter")
        self._multimeter.start()
        self._log_running_threads()
        self.fail_if(len(threading.enumerate()) != self._n_threads + 1,
                     "The multimeter did not restart properly")
        self.fail_if(not self._multimeter.is_running(), "The multimeter thread is not running")

    def test_voltage_dc(self):
        voltages = []
        self.log.debug(f"Get {self._N_SAMPLES} voltages")
        for _ in range(self._N_SAMPLES):
            response = self._send_command(b"VDC?")
            self.fail_if(not (response.startswith(b"VDC=") and
                              response.endswith(b"V" + self._TERMINATOR)),
                         f"Invalid response received '{response}'")
            voltages.append(float(response.strip()[4:-1]))
        self.log.debug(f"Voltages: {voltages}")
        self.fail_if(min(voltages) < 4.9, f"Voltage < 4.9 found: {min(voltages)}")
        self.fail_if(max(voltages) > 5.1, f"Voltage > 5.1 found: {max(voltages)}")

    def test_current_dc(self):
        currents = []
        self.log.debug(f"Get {self._N_SAMPLES} currents")
        for _ in range(self._N_SAMPLES):
            response = self._send_command(b"ADC?")
            self.fail_if(not (response.startswith(b"ADC=") and
                              response.endswith(b"A" + self._TERMINATOR)),
                         f"Invalid response received {response}")
            currents.append(float(response.strip()[4:-1]))
        self.log.debug(f"Currents: {currents}")
        self.fail_if(min(currents) < 0.39, f"Current < 0.39 found: {min(currents)}")
        self.fail_if(max(currents) > 0.41, f"Current > 0.41 found: {max(currents)}")

    def test_wrong_command(self):
        response = self._send_command(b"UNKNOWN_COMMAND?")
        self.fail_if(response != b"UNKNOWN COMMAND" + self._TERMINATOR,
                     "Wrong response received '{response}'")

    def teardown(self):
        self._multimeter.stop()
        self.fail_if(len(threading.enumerate()) != self._n_threads, "The multimeter did not stop")
        self.fail_if(self._multimeter.is_running(),
                     "The multimeter thread is still running after stop")


if __name__ == "__main__":

    import pylint

    TestMultimeterUdp().run(True)
    pylint.run_pylint([__file__])
