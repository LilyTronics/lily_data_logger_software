"""
Our own test suite class derived from the lily-unit-test test suite.
"""

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
    def wait_for(function_to_call, expected_result, timeout, interval):
        while timeout > 0:
            if function_to_call() == expected_result:
                return True
            time.sleep(interval)
            timeout -= interval
        return False
