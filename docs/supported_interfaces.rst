Supported interfaces
====================

The following interfaces are supported:

================ ===================================================================================
 Interface name   Description
================ ===================================================================================
 Serial port      This can be either a real serial port or a virtual com port (VCP) used by various

                  USB devices.
 Ethernet UDP     Ethernet connection using the UDP protocol.
 Ethernet TCP     Ethernet connection using the TCP protocol.
================ ===================================================================================

The interface name as shown in the table must be used in your instrument definition (case sensitive).

The TCP protocol is more stable because it is using hand shacking mechanism to determine if
messages are received correctly. The UDP protocol is not using this and messages can be lost
without knowing.

Both UDP and TCP do not support authentication or encryption.

All interfaces must be using messages using ASCII characters only.

The next chapters will describe more details about the interfaces.
