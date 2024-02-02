"""
Interfaces package.
"""

from src.models.interfaces import get_interface_by_name
from src.models.interfaces import get_interface_names
from tests.test_suite import TestSuite


class TestInterfaces(TestSuite):

    def test_interfaces(self):
        for name in get_interface_names():
            self.log.debug("{:12}: {}".format(name, get_interface_by_name(name)))
        interface = get_interface_by_name("Unknown interface name")
        self.fail_if(interface is not None, "Unknown interface name did not return None")


if __name__ == "__main__":

    TestInterfaces().run()
