"""
Do all the measurements according to configuration.
"""

import time
import threading

from src.models.instrument_pool import InstrumentPool


class MeasurementRunner:

    _MESSAGE_TYPE_STATUS = 'status'
    _MESSAGE_TYPE_VALUE = 'value'

    def __init__(self, configuration, callback):
        self._configuration = configuration
        self._callback = callback
        self._measurement_thread = None
        self._stop_event = threading.Event()

    def _send_callback(self, timestamp, message_type, identifier, value):
        # Wrapper to force uniform callback data
        self._callback(timestamp, message_type, identifier, value)

    def _create_instruments(self):
        self._send_callback(int(time.time()), self._MESSAGE_TYPE_STATUS, "Create instruments", 0)
        for i, measurement in enumerate(self._configuration.get_measurements()):
            settings = measurement[self._configuration.KEY_SETTINGS]
            instrument_data = self._configuration.get_instrument(
                settings[self._configuration.KEY_INSTRUMENT_ID])
            self._send_callback(
                int(time.time()),
                self._MESSAGE_TYPE_STATUS,
                f"Initialize instrument '{instrument_data[self._configuration.KEY_NAME]}'",
                i
            )
            instrument = InstrumentPool.create_instrument(instrument_data)
            instrument.initialize()
            instrument.start()

    def _process_response(self, measurement_id, response):
        request_time, measurement_name = measurement_id.split(" ")
        request_time = int(request_time)
        response_time = time.time()
        sample_time = self._configuration.get_sample_time()
        # We need to check if the timing is correct.
        # The response time should be within request_time + sample_time
        # If the response is too late, we send an error value for the original request time
        # and the measurement value to the next valid request time
        while request_time + sample_time < response_time:
            self._send_callback(request_time, self._MESSAGE_TYPE_VALUE, measurement_name,
                                "time error")
            request_time += sample_time
        self._send_callback(request_time, self._MESSAGE_TYPE_VALUE, measurement_name, response)

    def _requests_measurements(self, timestamp):
        measurements = self._configuration.get_measurements()
        for measurement in measurements:
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
        self._create_instruments()
        start_time = int(time.time())
        self._send_callback(start_time, self._MESSAGE_TYPE_STATUS, "Start measurements", 0)
        sample_start = start_time
        while not self._stop_event.is_set():
            self._requests_measurements(sample_start)
            while not self._stop_event.is_set():
                if time.time() - sample_start >= sample_time:
                    break
                if time.time() - start_time >= end_time:
                    self._stop_event.set()
                time.sleep(0.01)
            sample_start = int(time.time())
        self._send_callback(int(time.time()), self._MESSAGE_TYPE_STATUS, "Process finished", 0)

    def start(self):
        if not self.is_running():
            self._measurement_thread = threading.Thread(target=self._run_measurements)
            self._measurement_thread.daemon = True
            self._stop_event.clear()
            self._measurement_thread.start()

    def stop(self):
        if self.is_running():
            self._stop_event.set()
            self._measurement_thread.join()
        self._measurement_thread = None
        InstrumentPool.clear_instruments()

    def is_running(self):
        return self._measurement_thread is not None and self._measurement_thread.is_alive()


if __name__ == "__main__":

    import pylint

    from tests.unit_tests.test_models.test_measurement_runner import TestMeasurementRunner

    TestMeasurementRunner().run()
    pylint.run_pylint([__file__])
