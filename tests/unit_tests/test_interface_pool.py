"""
Test the interface pool.
"""

from src.models.interface_pool import InterfacePool
from src.models.interfaces.serial_port_interface import SerialPortInterface
from src.models.interfaces.tcp_client_interface import TcpClientInterface
from src.models.interfaces.udp_client_interface import UdpClientInterface
from src.models.list_serial_ports import get_available_serial_ports
from tests.unit_tests.lib.test_suite import TestSuite


class TestInterfacePool(TestSuite):

    def test_instantiating(self):
        try:
            _interface_pool = InterfacePool()
            self.fail("No run time error was generated, while we expected one")
        except RuntimeError as e:
            self.log.debug("Run time error generated as expected")
            self.log.debug("Run time error: {}".format(e))

    def test_serial_interface(self):
        self.log.debug("Get available serial ports")
        ports = get_available_serial_ports()
        self.log.debug("Found ports: {}".format(ports))
        interface_object2 = None
        for port_name in ports:
            self.log.debug("Create serial interface for port: {}".format(port_name))
            interface_object1 = InterfacePool.create_interface(SerialPortInterface, {"serial_port": port_name})
            self.fail_if(interface_object1 is interface_object2,
                         "Same interface for port {}, while we expect a new interface".format(port_name))
            self.log.debug("Try create a serial interface with the same port")
            interface_object2 = InterfacePool.create_interface(SerialPortInterface, {"serial_port": port_name})
            self.fail_if(interface_object1 is not interface_object2,
                         "A new interface object is created for the same port")

    def test_udp_interface(self):
        self.log.debug("Create UDP interfaces")
        ip_addresses = ["1.2.3.4", "5.6.7.8"]
        ip_ports = [17000, 18000]
        interface_object2 = None
        for ip_address in ip_addresses:
            for ip_port in ip_ports:
                self.log.debug("Create UDP interface with address: {}:{}".format(ip_address, ip_port))
                interface_object1 = InterfacePool.create_interface(UdpClientInterface,
                                                                   {"ip_address": ip_address, "ip_port": ip_port})
                self.fail_if(interface_object1 is interface_object2,
                             "Same interface for address {}:{}, while we expect a new interface".format(
                                 ip_address, ip_port))
                self.log.debug("Try create a UDP interface with the same address")
                interface_object2 = InterfacePool.create_interface(UdpClientInterface,
                                                                   {"ip_address": ip_address, "ip_port": ip_port})
                self.fail_if(interface_object1 is not interface_object2,
                             "A new interface object is created for the same address")

    def test_tcp_interface(self):
        self.log.debug("Create TCP interfaces")
        ip_addresses = ["1.2.3.4", "5.6.7.8"]
        ip_ports = [17000, 18000]
        interface_object2 = None
        for ip_address in ip_addresses:
            for ip_port in ip_ports:
                self.log.debug("Create TCP interface with address: {}:{}".format(ip_address, ip_port))
                interface_object1 = InterfacePool.create_interface(TcpClientInterface,
                                                                   {"ip_address": ip_address, "ip_port": ip_port})
                self.fail_if(interface_object1 is interface_object2,
                             "Same interface for address {}:{}, while we expect a new interface".format(
                                 ip_address, ip_port))
                self.log.debug("Try create a TCP interface with the same address")
                interface_object2 = InterfacePool.create_interface(TcpClientInterface,
                                                                   {"ip_address": ip_address, "ip_port": ip_port})
                self.fail_if(interface_object1 is not interface_object2,
                             "A new interface object is created for the same address")


if __name__ == "__main__":

    TestInterfacePool().run(True)
