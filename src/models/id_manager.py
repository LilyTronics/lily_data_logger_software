"""
Manages ID for various purposes
"""

import wx

from unit_test.test_suite import TestSuite


class IdManager(object):

    # View edit configuration
    ID_SAMPLE_TIME = 100
    ID_SAMPLE_TIME_UNITS = 101
    ID_END_TIME = 102
    ID_END_TIME_UNITS = 103
    ID_FIXED = 104
    ID_CONTINUOUS = 105
    ID_TOTAL_SAMPLES = 106

    _RESERVED_WIDGET_IDS = sorted(list(map(lambda y: getattr(wx, y), filter(lambda x: x.startswith("ID_"), dir(wx)))))
    _WIDGET_START_ID = 100
    _WIDGET_END_ID = 32000

    def __init__(self):
        # Prevent creating instances
        raise RuntimeError("No instance of this class is permitted")

    @classmethod
    def get_reserved_widgets_ids(cls):
        return cls._RESERVED_WIDGET_IDS


class TestIdManager(TestSuite):

    def test_id_manager_class(self):
        try:
            self.log.debug("Try create an instance")
            IdManager()
            self.fail("An instance of the class could be created, while not allowed")
        except RuntimeError:
            self.log.debug("Expected run time error was raised")

    def test_ids(self):
        values = []
        self.log.debug("Test if IDs are valid")
        for value in map(lambda x: getattr(IdManager, x), filter(lambda x: x.startswith("ID_"), dir(IdManager))):
            self.fail_if(value in IdManager.get_reserved_widgets_ids(), "The value is used in the reserved widgets")
            self.fail_if(value in values, "The value {} is already used".format(value))
            values.append(value)


if __name__ == "__main__":

    TestIdManager().run()
