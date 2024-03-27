Special commands
================

In the command list of your instrument definition you can use one of the following special commands:

========================== ======================================= ==============================
 Command                    Description                             Possible values
========================== ======================================= ==============================
 instrument_delay:<value>   Insert a delay of a number of seconds   Any number greater than zero.

                                                                    Can be a fractional number.
 interface:toggle_dtr       Toggle the DTR line on a serial port.
========================== ======================================= ==============================

Examples:

.. code-block:: json

  "command_list": [
    {
      "command": "interface:toggle_dtr"
    },
    {
      "command": "instrument_delay:1.5"
    }
  ]
