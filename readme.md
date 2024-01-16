# Lily Data Logger Studio

Universal data logger software aiming to work with any kind of electronics measurement device.
Not only logging data but also controlling instruments (process automation).

## Installation

There will be an executable for Windows available when the first release is ready (portable).
Download the executable and run it. There is no need to install any software.
Settings and logs are stored in: `C:\users\your_name\LilyDataLoggerStudio`.

## Instruments

The following instruments are included in the application:
* Power supply: TTi PL303QMD-P (USB virtual COM port)
* Simulators (for testing/demo):
  * Multimeter giving random values for voltage and current
  * Temperature chamber that can be set to heat up or cool down to a specified temperature.

Note that not all commands for the instruments are implemented.
A set of the most practical commands are chosen.

On request, we can add an instrument for you, or help you create instrument files.
Contact us for more information at: info@lilytronics.nl

## Releases

No releases yet, still work in progress.
Things to do for the first release:

* Add/edit/delete instruments
* Add/edit/delete process steps
* Add/delete measurements
* Start/Stop data logger
* Export measurements to CVS
* Check instruments
* Add the following instruments:
  * TDS220 oscilloscope (or compatible TDS200, TDS1000 and TDS2000, they have the same interface)
  * NI USB-6009 (requires drivers from NI)
  * Protek 506 digital multimeter
  * Arduino Uno IO module (reading analog voltages, reading and writing digital IO, sketch for the Arduino Uno is included in this repo)
 
# Adding your own instruments

You can add your own instruments using JSON files. Simply make a definition for your instrument and store the file in
the folder: `C:\users\your_name\LilyDataLoggerStudio`.
The application will load any JSON file that contains an instrument definition.

A JSON file can be created in a text editor.

Instrument file format:

```json
{
  "name": "my power supply",
  "info": "Some detailed information that you would like to show in the application when editing the instrument",
  "interface": {
    "type": "serial",
    "settings": {
      "baud_rate": 115200,
      "time_out": 2
    }
  },
  "channels": [
    {
      "name": "get voltage",
      "type": "input",
      "command": "U?\n",
      "response": "U={float}V\n"
    },
    {
      "name": "set voltage",
      "type": "output",
      "command": "U={float:3}V\n",
      "response": "OK\n"
    }
  ]
}
```

This JSON file describes a simple power supply instrument with 2 channels for reading and setting the voltage.

The name is obviously the name of the instrument, this usually is the manufacturer type number.

The interface section defines the interface type and the settings.
Settings that are not specified are set to their default values (like number of stop bits, parity mode, etc.).
The settings can be overridden in the application.

The channels sections describe the channels.

The first channel is for reading the output voltage (get voltage).
The type is input and the command and expected response are defined.
The keyword `{float}` indicates we expect a floating point value there.
The application will try to match the actual response with this definition and returns the extracted value as a floating point.

The second channel is for setting the desired output voltage (set voltage). This can be used in process automation.
The command has a keyword `{float:3}` the desired value, will be converted to a string with a floating point representation.
The representation will have as many digits as required before the decimal point and 3 digits behind the digital point.
For example if the desired value is 3.5V this will be sent as: `U=3.500V`.

There are a number of variations possible:

* `{float}`: a floating point with as many digits as required.
* `{float:3}`: a floating point with as many digits as required before the decimal point and 3 digits behind the decimal point
* `{int}`: an integer with as many digits as required.
* `{str}`: a literal string value.

## Development

Requirements for running the software:

* Python (>= 3.10)
* Upgrade pip: python -m pip install --upgrade pip
* pip install -r requirements.txt

In `unit_test` is a script for running the unit tests `run_unit_tests.py`
Test reports are written to `unit_test/test_reports`.

2023 - LilyTronics (https://lilytronics.nl)
