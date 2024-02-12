"""
Do all the measurements according to configuration.
"""

import time
import threading


class MeasurementRunner(object):

    def __init__(self, configuration, callback):
        self._configuration = configuration
        self._callback = callback
        self._measurement_thread = None
        self._stop_event = threading.Event()

    def _run_measurements(self):
        self._callback(0, "Process starting")
        measurements = self._configuration.get_measurements()
        sample_time = self._configuration.get_sample_time()
        end_time = self._configuration.get_end_time()
        do_sample = True
        start_time = time.time()
        sample_start = time.time()
        while not self._stop_event.is_set():
            if do_sample:
                for measurement in measurements:
                    self._callback(time.time() - start_time, "Process  measurement: {}".format(
                        measurement[self._configuration.KEY_NAME]))
                do_sample = False
            time.sleep(0.05)
            interval = time.time() - sample_start
            if interval >= sample_time:
                sample_start = time.time()
                do_sample = True
            duration = time.time() - start_time
            if duration >= end_time:
                break
        self._callback(time.time() - start_time, "Process finished")

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

    from src.models.configuration import Configuration

    def _callback(*args):
        print(args)

    conf = Configuration()
    conf.load_from_file("..\\..\\tests\\test_files\\test_configuration.json")
    conf.set_sample_time(2)
    conf.set_end_time(8)

    mr = MeasurementRunner(conf, _callback)

    mr.start()
    print(mr.is_running())
    time.sleep(5)
    # Abort
    mr.stop()
    print(mr.is_running())

    mr.start()
    print(mr.is_running())
    # Let it run until finished
    while mr.is_running():
        time.sleep(1)
