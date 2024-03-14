"""
Base class for all the interfaces.
"""

import threading


class Interface:

    def __init__(self, params_to_match):
        self._params_to_match = params_to_match
        self._lock = threading.RLock()

    def __del__(self):
        try:
            self.close()
        except (Exception, ):
            pass

    def raise_connection_exception(self, params):
        raise Exception(f"Could not connect to {params}")

    def raise_timeout_exception(self):
        raise Exception("Error receiver timeout")

    def send_command(self, command, expect_response, pre_response, post_response):
        raise NotImplementedError("This method must be implemented in the derived class")

    def is_open(self):
        raise NotImplementedError("This method must be implemented in the derived class")

    def open(self):
        raise NotImplementedError("This method must be implemented in the derived class")

    def close(self):
        raise NotImplementedError("This method must be implemented in the derived class")

    def is_match(self, params):
        is_match = True
        for key in self._params_to_match.keys():
            if key not in params.keys() or params[key] != self._params_to_match[key]:
                is_match = False
                break
        return is_match

    @classmethod
    def get_settings_controls(cls):
        raise NotImplementedError("This method must be implemented in the derived class")

    def acquire_lock(self):
        self._lock.acquire()

    def release_lock(self):
        self._lock.release()


if __name__ == "__main__":

    from tests.unit_tests.test_models.test_interface import TestInterface

    TestInterface().run(True)
