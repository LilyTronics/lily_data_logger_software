"""
Manages ID for various purposes
"""

from unit_test.test_suite import TestSuite


class IdManager(object):

    def __init__(self):
        # Prevent creating instances
        raise RuntimeError("No instance of this class is permitted")


class TestIdManager(TestSuite):

    def test_id_manager_class(self):
        try:
            self.log.debug("Try create an instance")
            IdManager()
            self.fail("An instance of the class could be created, while not allowed")
        except RuntimeError as e:
            self.log.debug("Expected run time error was raised")


if __name__ == "__main__":

    TestIdManager().run()
