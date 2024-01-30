# Lily Data Logger Studio CE (Community Edition)

Universal data logger software aiming to work with any kind of electronics measurement device.

## Installation

There will be an executable for Windows available when the first release is ready (portable).
Download the executable and run it. There is no need to install any software.
Settings and logs are stored in: `C:\users\your_name\LilyDataLoggerStudio`.

## Instruments

The following instruments are included in the application:
* Arduino Uno DAQ: reading analog voltages, reading and writing digital IO, sketch for the Arduino Uno is included in this repo.
* Simulators (for testing/demo):
  * Multimeter giving random values for voltage and current

Note that not all commands for the instruments are implemented.
A set of the most practical commands are chosen.

On request, we can add an instrument for you, or help you create instrument files.
Contact us for more information at: info@lilytronics.nl

## Releases

No releases yet, still work in progress.

# Adding your own instruments

You can add your own instruments. A manual for that will be available on the first release.

## Development

Requirements for running the software:

* Python (>= 3.10)
* Upgrade pip: python -m pip install --upgrade pip
* pip install -r requirements.txt

In `unit_test` is a script for running the unit tests `run_unit_tests.py`
Test reports are written to `unit_test/test_reports`.

2023 - LilyTronics (https://lilytronics.nl)
