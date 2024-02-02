"""
Test for the ID manager.
"""

from src.models.id_manager import IdManager
from tests.test_suite import TestSuite


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
