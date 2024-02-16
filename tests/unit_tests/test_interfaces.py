"""
Interfaces package.
"""

from src.models.interfaces import Interfaces
from tests.unit_tests.lib.test_suite import TestSuite


class TestInterfaces(TestSuite):

    def test_interfaces(self):
        for name in Interfaces.get_interface_names():
            self.log.debug(f"{name:12}: {Interfaces.get_interface_by_name(name)}")
        interface = Interfaces.get_interface_by_name("Unknown interface name")
        self.fail_if(interface is not None, "Unknown interface name did not return None")


if __name__ == "__main__":

    import pylint

    TestInterfaces().run()
    pylint.run_pylint([__file__])
