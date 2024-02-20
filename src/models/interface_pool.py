"""
Create a pool with all required interfaces.
Some interfaces can be used by multiple instruments.
For example if we have an RS-485 bus with multiple instruments connected to that bus,
there is only one interface to the RS-485 port, but used by multiple instruments.
This pool prevents creating multiple interfaces to the same port.
"""

import threading

from src.models.interfaces import Interfaces


class InterfacePool:

    _INTERFACES = []
    _LOCK = threading.RLock()

    def __init__(self):
        # Prevent creating instances
        raise RuntimeError("Creating an instance of this class is not permitted")

    @classmethod
    def create_interface(cls, interface_name, parameters):
        with cls._LOCK:
            interface_object = None
            interface_class = Interfaces.get_interface_by_name(interface_name)
            matches = list(filter(lambda x: isinstance(x, interface_class), cls._INTERFACES))
            if len(matches) > 0:
                for instance in matches:
                    if instance.is_match(parameters):
                        interface_object = instance
                        break
            if interface_object is None:
                interface_object = interface_class(**parameters)
                cls._INTERFACES.append(interface_object)
        return interface_object

    @classmethod
    def clear_interfaces(cls):
        cls._INTERFACES.clear()


if __name__ == "__main__":

    import pylint
    from tests.unit_tests.test_interface_pool import TestInterfacePool

    TestInterfacePool().run(True)
    pylint.run_pylint([__file__])
