"""
Create a pool with all required interfaces.
Some interfaces can be used by multiple instruments.
For example if we have an RS-485 bus with multiple instruments connected to that bus,
there is only one interface to the RS-485 port, but used by multiple instruments.
This pool prevents creating multiple interfaces to the same port.
"""

import threading


class InterfacePool(object):

    _INTERFACES = []
    _LOCK = threading.RLock()

    def __init__(self):
        # Prevent creating instances
        raise RuntimeError("Creating an instance of this class is not permitted")

    @classmethod
    def create_interface(cls, interface_class, parameters):
        try:
            cls._LOCK.acquire()
            interface_object = None
            matches = list(filter(lambda x: isinstance(x, interface_class), cls._INTERFACES))
            if len(matches) > 0:
                for instance in matches:
                    if instance.is_match(parameters):
                        interface_object = instance
                        break
            if interface_object is None:
                interface_object = interface_class(**parameters)
                cls._INTERFACES.append(interface_object)
        finally:
            cls._LOCK.release()
        return interface_object


if __name__ == "__main__":

    from tests.unit_tests.test_interface_pool import TestInterfacePool

    TestInterfacePool().run(True)
