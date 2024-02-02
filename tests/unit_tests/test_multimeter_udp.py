"""
Test multimeter using UDP interface.
"""

import socket
import threading

from src.simulators.multimeter_udp import MultimeterUdp
from src.simulators.simulator_settings import SimulatorSettings
from tests.test_suite import TestSuite


class TestMultimeterUdp(TestSuite):

    _RX_TIME_OUT = 0.5
    _RX_BUFFER_SIZE = 1500
    _N_SAMPLES = 10
    _TERMINATOR = b"\n"

    def _log_running_threads(self):
        self.log.debug("Running threads: {}".format(", ".join(map(lambda x: str(x), threading.enumerate()))))

    def _send_command(self, command):
        self._socket.sendto(command + self._TERMINATOR,
                            (SimulatorSettings.MultimeterUdp.IP, SimulatorSettings.MultimeterUdp.PORT))
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
        self.fail_if(len(threading.enumerate()) != self._n_threads + 1, "The multimeter did not start properly")
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
        self.fail_if(self._multimeter.is_running(), "The multimeter thread is still running after stop")

        self.log.debug("Stop multimeter while not running")
        self._multimeter.stop()

        self.log.debug("Restart multimeter")
        self._multimeter.start()
        self._log_running_threads()
        self.fail_if(len(threading.enumerate()) != self._n_threads + 1, "The multimeter did not restart properly")
        self.fail_if(not self._multimeter.is_running(), "The multimeter thread is not running")

    def test_voltage_dc(self):
        voltages = []
        self.log.debug("Get {} voltages".format(self._N_SAMPLES))
        for i in range(self._N_SAMPLES):
            response = self._send_command(b"VDC?")
            self.fail_if(not (response.startswith(b"VDC=") and response.endswith(b"V" + self._TERMINATOR)),
                         "Invalid response received '{}'".format(response))
            voltages.append(float(response.strip()[4:-1]))
        self.log.debug("Voltages: {}".format(voltages))
        self.fail_if(min(voltages) < 4.9, "Voltage < 4.9 found: {}".format(min(voltages)))
        self.fail_if(max(voltages) > 5.1, "Voltage > 5.1 found: {}".format(max(voltages)))

    def test_current_dc(self):
        currents = []
        self.log.debug("Get {} currents".format(self._N_SAMPLES))
        for i in range(self._N_SAMPLES):
            response = self._send_command(b"ADC?")
            self.fail_if(not (response.startswith(b"ADC=") and response.endswith(b"A" + self._TERMINATOR)),
                         "Invalid response received {}".format(response))
            currents.append(float(response.strip()[4:-1]))
        self.log.debug("Currents: {}".format(currents))
        self.fail_if(min(currents) < 0.39, "Current < 0.39 found: {}".format(min(currents)))
        self.fail_if(max(currents) > 0.41, "Current > 0.41 found: {}".format(max(currents)))

    def test_wrong_command(self):
        response = self._send_command(b"UNKNOWN_COMMAND?")
        self.fail_if(response != b"UNKNOWN COMMAND" + self._TERMINATOR, "Wrong response received '{}'".format(response))

    def teardown(self):
        self._multimeter.stop()
        self.fail_if(len(threading.enumerate()) != self._n_threads, "The multimeter did not stop")
        self.fail_if(self._multimeter.is_running(), "The multimeter thread is still running after stop")


if __name__ == "__main__":

    TestMultimeterUdp().run(True)
