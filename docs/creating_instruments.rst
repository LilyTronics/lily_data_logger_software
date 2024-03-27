Creating your own instruments
=============================

It is impossible to have all instruments supported out of the box. Therefore there is a way to add
your own instruments. The instrument must comply to the following specifications:

* The communication protocol must be using ASCII characters.
* The interface should be serial, UDP or TCP.
* There must not be a user login procedure for the instrument (no authentication needed).

The instruments can be added by creating a JSON formatted file (driver) that defines all the
measurements for an instrument.

There are two ways to create a driver. From scratch or use an existing driver.

From scratch
------------

In this example we create a driver from scratch. This driver is for the Tektronix TDS220 oscilloscope.
We use the serial port to communicate with the instrument.

Instrument files must be stored in the user folder. Let's say your name is 'Joe', the following
folder should be present:

.. code-block:: console

    Windows: C:\Users\joe\LilyDataLoggerStudioCE
    Ubuntu : /home/joe/LilyDataLoggerStudioCE


Using an existing driver
------------------------

You can use an already existing driver. This is convenient if the instrument you want to add is
similar to an already existing one. The instrument must be added to the configuration first.

In the toolbar on the main view is a download button (next to the export CSV). Select an instrument
from the instruments list and click the download button.
As example below is part of the download of the Arduino DAQ driver.

.. code-block:: json

  {
    "name": "Arduino DAQ",
    "info": "Read and write digital IO and read analog values with an Arduino",
    "interface": {
      "type": "Serial port",
      "settings": {
        "baud_rate": 115200
      }
    },
    "initialize": [
      {
        "command": "interface:toggle_dtr"
      },
      {
        "command": "instrument_delay:2"
      },
      {
        "command": "rd2\n",
        "response": "{int}\n"
      }
    ],
    "channels": [
      {
        "name": "D2 get state",
        "type": "input",
        "command_list": [
          {
            "command": "rd2\n",
            "response": "{int}\n"
          }
        ]
      },
      {
        "name": "A0 get voltage",
        "type": "input",
        "command_list": [
          {
            "command": "ra0\n",
            "response": "{float}\n"
          }
        ]
      }
    ]
  }

Not all channels are shown in the example. After download you can modify it to you needs.
