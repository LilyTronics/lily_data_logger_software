Introduction
============

This is the user manual for the Lily Data Logger Studio CE. CE stands for Community Edition,
which is the free open source edition. The source code is available on GitHub and the software
can be used free of charge for personal and professional use.

Included in the application are simulators that can be used to try the software and all of the
features. Working with the simulators is covered in this manual.

Features
--------

* Logging data (measurements) in a table.
* Free and open source for personal and professional use.
* Build in drivers for the following instruments:
  * Arduino DAQ: reading analog voltages, reading and writing digital IO. A sketch for the Arduino is included.
  * Multimeter simulator giving random values for voltage and current, for testing measurements.
* Fixed end time or continuous measurement.
* Smallest sample interval: 1 second.
* Adding your own instrument drivers (see manual)
* Data from the table can be copied and pasted to a spreadsheet (Excel, LibreOffice, etc.).
* Export to CSV for using data in other applications (databases, scripting, etc.).

About GPIB...
-------------

We get some questions if GPIB will be supported. GPIB is a standarized communication bus for instruments. But the standardization is only on the GPIB part.
The command and response structure are standarized. What is not standarized is the GPIB PC controller. In the past PCs used ISA cards.
Now a days you need to have a USB to GPIB controller. And in this controller lies the problem. Supporting the GPIB protocol is fairly easy.
Supporting all available GPIB controllers on the market is a headache. Every GPIB controller requires its own specific driver.
And to test it, we need a sample of each controller available. And those controllers are not cheap. So for now it is not very feasible to have GPIB supported.
But... if someone is willing to donate a GPIB controller, we will be happy to add support for it.
