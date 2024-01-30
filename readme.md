# Lily Data Logger Studio CE (Community Edition)

Universal data logger software aiming to work with any kind of electronics measurement device.

## Editions

The Lily Data Logger Studio has two editions:

* CE: Community Edition.
  * A simple tool that only logs data (measurements).
  * Free and open source.
  * Is provides as is and has no support.


* XE: eXtended Edition.
  * All features of the CE.
  * Extra support for the following instruments:
    * Tektronics TD220 (or similar: TDS200/TDS1000/TDS2000).
    * TTi PL303QMD-P power supply.
    * National Instruments USB-6009 DAQ (requires NI drivers, not included, installation manual available).
    * Protek 506 multimeter.
    * Temperature chamber simulator (for testing the process control feature). 
  * Process control automation. Create and run processes to control your entire test setup (test automation).
  * Support from LilyTronics.
    * Help when using the application and creating processes.
    * Help for adding your instruments.

The CE version is available through GitHub. The XE version is sold through our website at https://lilytronics.nl.

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
