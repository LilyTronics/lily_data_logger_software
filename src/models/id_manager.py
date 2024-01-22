"""
Manages ID for various purposes
"""

import threading
import wx

from unit_test.test_suite import TestSuite


class IdManager(object):

    _WIDGET_IDS = []
    _WIDGET_START_ID = 100
    _WIDGET_END_ID = 32000
    _RESERVED_WIDGET_IDS = sorted(list(map(lambda y: getattr(wx, y), filter(lambda x: x.startswith("ID_"), dir(wx)))))
    _LOCK = threading.RLock()

    def __init__(self):
        # Prevent creating instances
        raise RuntimeError("No instance of this class is permitted")

    @classmethod
    def get_reserved_widgets_ids(cls):
        return cls._RESERVED_WIDGET_IDS

    @classmethod
    def get_widget_id(cls, start=_WIDGET_START_ID):
        new_id = start
        while new_id <= cls._WIDGET_END_ID:
            cls._LOCK.acquire()
            try:
                if new_id not in cls._RESERVED_WIDGET_IDS and new_id not in cls._WIDGET_IDS:
                    cls._WIDGET_IDS.append(new_id)
                    break
            finally:
                cls._LOCK.release()
            new_id += 1
        else:
            raise RuntimeError("Could not get a free ID for the widget")
        return new_id


class TestIdManager(TestSuite):

    def test_id_manager_class(self):
        try:
            self.log.debug("Try create an instance")
            IdManager()
            self.fail("An instance of the class could be created, while not allowed")
        except RuntimeError:
            self.log.debug("Expected run time error was raised")

    def test_widget_ids(self):
        self.log.debug("Generate some standard widget IDs")
        for i in range(10):
            new_id = IdManager.get_widget_id()
            self.fail_if(i + 100 != new_id, "Failed to generate widget ID {} got {}".format(i + 100, new_id))
        self.log.debug("Try to generate some IDs matching reserved IDs, should be skipped")
        for i in range(10):
            new_id = IdManager.get_widget_id(5000)
            self.fail_if(new_id in IdManager.get_reserved_widgets_ids(),
                         "The generated ID is a reserved ID {}".format(new_id))
        self.log.debug("Try to generate some IDs outside max limit")
        i = 0
        for i in range(10):
            try:
                IdManager.get_widget_id(31995)
            except RuntimeError:
                self.log.debug("Expected run time error was raised")
                break
        self.fail_if(i == 9, "No run time error was raised, while it was expected")

    def _get_widget_id(self):
        self._lock.acquire()
        try:
            self._widget_ids.append(IdManager.get_widget_id())
        finally:
            self._lock.release()

    def test_multi_threading(self):
        self._widget_ids = []
        self._lock = threading.RLock()
        self.log.debug("Test generate IDs from multiple threads")
        threads = []
        for i in range(500):
            threads.append(self.start_thread(self._get_widget_id))
        while True in list(map(lambda x: x.is_alive(), threads)):
            self.sleep(0.1)
        self.fail_if(len(self._widget_ids) != 500,
                     "The number of IDs is not equal to 500: {}".format(len(self._widget_ids)))
        for i in self._widget_ids:
            count = self._widget_ids.count(i)
            self.fail_if(count != 1, "The ID {} was found more than once: {}".format(i, count))


if __name__ == "__main__":

    TestIdManager().run()
