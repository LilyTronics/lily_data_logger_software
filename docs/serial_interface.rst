Serial interface
================

The serial port interface is using a cross platform library (pySerial).
The serial port can have the following parameters:

============= ================================= ================================= =========
 Parameter     Description                       Possible values                   Default
============= ================================= ================================= =========
 serial_port   The name of the serial port       Determined by the OS
 baud_rate     The baud rate (speed)             See below                         19200
 parity        What parity to use                None, Odd, Even, Mark, Space      None
 stop_bits     Number of stop bits               1, 1.5, 2                         1
 data_bits     Number of data bits               5, 6, 7, 8                        8
 rx_timeout    Receiver time out in seconds      any numeric value larger than 0   3
 tx_timeout    Transmitter time out in seconds   any numeric value larger than 0   3
============= ================================= ================================= =========

The parameter names used in your instrument definition must match the names in the table.

The serial port name is determined by the OS. On Windows it will be 'COM1', 'COM2', etc.
On linux based OS it will be like: '/dev/ttyS0', '/dev/ttyUSB0', ect.

The available serial ports are detected automatically. If your serial port is not listed, check
if the serial port is available in your system.

On Windows, you can check the Device Manager and
look for 'Ports (COM & LPT)'. If your serial port is not listed there, you may need to install a
driver first.

On Linux, serial ports are listed in the folder: '/dev'. You can list serial ports by
using the command: ``ls /dev/tty*``. If your port is not listed there, then the device is not supported
by Linux. In Linux you also need access rights to the serial port. In Ubuntu all serial ports
belong to the group ``dailout``. To access the serial ports, you need to be a member of that group.
To do so you need to add your user to that group with the command: ``sudo adduser <username> dialout``.
Where '<username>' is the name of your user. For example if the username you use is 'joe', then the
command will be: ``sudo adduser joe dialout``. To make the changes effective you need to log out and
log in.

If your serial port is available and you have access to it, but the serial port is still not available
in the application, the serial port may be in use by another application. Only one application can
use a serial port. Close all applications that use the serial port.

The baud rate can be set to one of the following values:

1200, 1800, 2400, 4800, 9600, 14400, 19200, 28800, 31250, 38400, 57600, 76800, 115200, 128000,
230400, 250000, 256000, 460800, 500000, 576000, 921600, 1000000

These are the most common values used when creating this application. Should you need a value
that is not listed, let us know and we will add it.

The names of the parity values, must be matching one of the names as shown in the table (case sensitive).
