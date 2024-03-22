"""
Do all the measurements according to configuration.
"""

import time
import threading

from src.models.instrument_pool import InstrumentPool


class MeasurementRunner:

    MESSAGE_TYPE_STATUS_CREATE = "create"
    MESSAGE_TYPE_STATUS_ERROR = "error"
    MESSAGE_TYPE_STATUS_FINISHED = "finished"
    MESSAGE_TYPE_STATUS_INIT = "init"
    MESSAGE_TYPE_STATUS_START = "start"
    MESSAGE_TYPE_VALUE = "value"

    def __init__(self, configuration, callback):
        self._configuration = configuration
        self._callback = callback
        self._measurement_thread = None
        self._stop_event = threading.Event()
        self._elapsed_time = 0

    def _send_callback(self, timestamp, message_type, identifier, value):
        # Wrapper to force uniform callback data
        self._callback(timestamp, message_type, identifier, value)

    def _create_instruments(self):
        instruments = self._configuration.get_measurements()
        self._send_callback(int(time.time()), self.MESSAGE_TYPE_STATUS_CREATE, "Create instruments",
                            len(instruments))
        for i, measurement in enumerate(instruments):
            settings = measurement[self._configuration.KEY_SETTINGS]
            instrument_data = self._configuration.get_instrument(
                settings[self._configuration.KEY_INSTRUMENT_ID])
            self._send_callback(
                int(time.time()),
                self.MESSAGE_TYPE_STATUS_INIT,
                f"Initialize instrument '{instrument_data[self._configuration.KEY_NAME]}'",
                i
            )
            try:
                instrument = InstrumentPool.create_instrument(instrument_data)
                if not instrument.is_running():
                    instrument.initialize()
                    instrument.start()
            except Exception as e:
                message = "ERROR: initializing instrument "
                message += f"'{instrument_data[self._configuration.KEY_NAME]}'\n{e}"
                self._send_callback(
                    int(time.time()),
                    self.MESSAGE_TYPE_STATUS_ERROR,
                    message,
                    i
                )
                return False
        return True

    def _process_response(self, measurement_id, response):
        request_time, measurement_name = measurement_id.split(" ", 1)
        request_time = int(request_time)
        response_time = time.time()
        sample_time = self._configuration.get_sample_time()
        # We need to check if the timing is correct.
        # The response time should be within request_time + sample_time
        # If the response is too late, we send an error value for the original request time
        # and the measurement value to the next valid request time
        while request_time + sample_time < response_time:
            self._send_callback(request_time, self.MESSAGE_TYPE_VALUE, measurement_name,
                                "time error")
            request_time += sample_time
        self._send_callback(request_time, self.MESSAGE_TYPE_VALUE, measurement_name, response)

    def _requests_measurements(self, timestamp):
        measurements = self._configuration.get_measurements()
        for measurement in measurements:
            if self._stop_event.is_set():
                break
            settings = measurement[self._configuration.KEY_SETTINGS]
            instrument_data = self._configuration.get_instrument(
                settings[self._configuration.KEY_INSTRUMENT_ID])
            instrument = InstrumentPool.create_instrument(instrument_data)
            instrument.process_channel(settings[self._configuration.KEY_MEASUREMENT], value=None,
                                       callback=self._process_response,
                                       callback_id=f"{timestamp} "
                                                   f"{measurement[self._configuration.KEY_NAME]}")

    def _run_measurements(self):
        sample_time = self._configuration.get_sample_time()
        end_time = self._configuration.get_end_time()
        InstrumentPool.clear_instruments()
        if self._create_instruments():
            start_time = int(time.time())
            self._send_callback(start_time, self.MESSAGE_TYPE_STATUS_START, "Start measurements", 0)
            sample_start = start_time
            while not self._stop_event.is_set():
                self._requests_measurements(sample_start)
                while not self._stop_event.is_set():
                    if time.time() - sample_start >= sample_time:
                        break
                    self._elapsed_time = time.time() - start_time
                    if self._elapsed_time >= end_time:
                        self._stop_event.set()
                    time.sleep(0.01)
                sample_start = int(time.time())
        self._send_callback(int(time.time()), self.MESSAGE_TYPE_STATUS_FINISHED,
                            "Process finished", 0)
        self._clean_up()

    def _clean_up(self):
        self._measurement_thread = None
        InstrumentPool.clear_instruments()

    ##########
    # Public #
    ##########

    def update_configuration(self, configuration):
        if not self.is_running():
            self._configuration = configuration

    def start(self):
        if not self.is_running() and len(self._configuration.get_measurements()) > 0:
            self._measurement_thread = threading.Thread(target=self._run_measurements)
            self._measurement_thread.daemon = True
            self._stop_event.clear()
            self._measurement_thread.start()

    def stop(self):
        if self.is_running():
            self._stop_event.set()
            self._measurement_thread.join()
        self._clean_up()

    def is_running(self):
        return self._measurement_thread is not None and self._measurement_thread.is_alive()

    def get_elapsed_time(self):
        return self._elapsed_time


if __name__ == "__main__":

    from tests.unit_tests.test_models.test_measurement_runner import TestMeasurementRunner

    TestMeasurementRunner().run()
