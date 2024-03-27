Ethernet UDP interface
======================

This interface is using the standard Python socket library. This interface transfers packages
over an Ethernet connection using the UDP protocol. The UDP protocol is not a reliable protocol and
messages can be lost without knowing it. The advantage is that UDP is faster than TCP.
The interface has the following parameters:

================ ================================= ================================== =========
 Parameter        Description                       Possible values                    Default
================ ================================= ================================== =========
 ip_address       The IP address or hostname        IPv4 address like 192.168.1.1 or

                                                    a hostname that is linked to an

                                                    IP address
 ip_port          A numeric value                   Any number that is not used
 rx_timeout       Receiver timeout in seconds       Any numeric value greater than 0   3
 rx_buffer_size   The buffer size in bytes          Any numeric value greater than 0   1500
================ ================================= ================================== =========

The parameter names used in your instrument definition must match the names in the table.

The IP address should be an IPv4 address. We have no idea if it works with IPv6 (not tested).
Names can also be used but they must be linked to an IP address usually by a DNS service.

The port number should be a number that is not used. Port numbers 1 to 1023 are privileged and
usually require administrator rights. Most of the port numbers 1 to 1023 are reserved for specific
services (like port 80 for HTTP and 433 for HTTPS). But also other services like databases can use
specific ports. There are tools that can show what ports are used in your system.

For Windows you can use the command: ``netstat -aon``.

For Ubuntu you can use the command: ``ss -an``.

The RX buffer size depends on how big the messages are that are send between the PC and the instrument.
Usually 1500 is large enough. Should you run into some problems, you can increase this.
