"""
Do all the measurements according to configuration.
"""

import time
import threading

from src.models.instrument_pool import InstrumentPool
from src.models.time_converter import TimeConverter


class MeasurementRunner:

    def __init__(self, configuration, callback):
        self._configuration = configuration
        self._callback = callback
        self._measurement_thread = None
        self._stop_event = threading.Event()

    def _create_instruments(self):
        self._callback(TimeConverter.get_timestamp(), "Create instruments")
        for measurement in self._configuration.get_measurements():
            settings = measurement[self._configuration.KEY_SETTINGS]
            instrument_data = self._configuration.get_instrument(
                settings[self._configuration.KEY_INSTRUMENT_ID])
            self._callback(
                TimeConverter.get_timestamp(),
                f"Initialize instrument '{instrument_data[self._configuration.KEY_NAME]}'")
            instrument = InstrumentPool.create_instrument(instrument_data)
            instrument.initialize()

    def _requests_measurements(self):
        measurements = self._configuration.get_measurements()
        timestamp = TimeConverter.get_timestamp()
        for measurement in measurements:
            self._callback(
                timestamp,
                f"Request  measurement: '{measurement[self._configuration.KEY_NAME]}'"
            )

    def _run_measurements(self):
        sample_time = self._configuration.get_sample_time()
        end_time = self._configuration.get_end_time()
        InstrumentPool.clear_instruments()
        self._create_instruments()
        self._callback(TimeConverter.get_timestamp(), "Start measurements")
        start_time = time.time()
        while not self._stop_event.is_set():
            sample_start = time.time()
            self._requests_measurements()
            while not self._stop_event.is_set():
                if time.time() - sample_start >= sample_time:
                    break
                if time.time() - start_time >= end_time:
                    self._stop_event.set()
        self._callback(TimeConverter.get_timestamp(), "Process finished")

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

    def is_running(self):
        return self._measurement_thread is not None and self._measurement_thread.is_alive()


if __name__ == "__main__":

    import pylint

    from tests.unit_tests.test_models.test_measurement_runner import TestMeasurementRunner

    TestMeasurementRunner().run()
    pylint.run_pylint([__file__])
