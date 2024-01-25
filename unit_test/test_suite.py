"""
Our own test suite class derived from the lily-unit-test test suite.
"""

import types
import lily_unit_test
import threading
import time

from unit_test.gui_unit_test import GuiUnitTest


class TestSuite(lily_unit_test.TestSuite):
    
    def __init__(self, *args):
        super().__init__(*args)
        self.gui = GuiUnitTest()

    @staticmethod
    def start_thread(target, args=()):
        t = threading.Thread(target=target, args=args)
        t.daemon = True
        t.start()
        return t

    @staticmethod
    def sleep(sleep_time):
        time.sleep(sleep_time)

    @staticmethod
    def wait_for(object_to_check, expected_result, timeout, interval):
        while timeout > 0:
            if callable(object_to_check):
                result = object_to_check()
            else:
                result = object_to_check
            if result == expected_result:
                return True
            time.sleep(interval)
            timeout -= interval
        return False


if __name__ == "__main__":

    class TestTestSuite(TestSuite):

        def test_start_thread(self):
            def _test_thread():
                t = 0.5
                while t > 0:
                    self.sleep(0.01)
                    t -= 0.01

            start = time.perf_counter()
            thread = self.start_thread(_test_thread)
            while thread.is_alive():
                self.sleep(0.01)
            end = time.perf_counter()
            self.fail_if(not (0.4 < (end - start) < 0.6), "Thread did not run")

        def test_wait_for(self):
            def _test_function():
                self._counter += 1
                return self._counter

            def _test_thread():
                self.sleep(0.2)
                self._object_to_check = True

            self._counter = 0
            self.wait_for(_test_function, 3, 1, 0.1)
            self.fail_if(self._counter != 3, "Counter has the wrong value")

            self._object_to_check = False
            self.start_thread(_test_thread)
            self.wait_for(self._object_to_check, True, 1, 0.1)
            self.fail_if(not self._object_to_check, "Object value did not change")


    TestTestSuite().run()