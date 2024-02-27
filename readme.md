# Lily Data Logger Studio CE (Community Edition)

Universal data logger software aiming to work with any kind of electronics measurement device (mulitmeters, oscilloscopes, power supplies, etc.).

## Releases

Coming up V1.0.0:

[![GitHub milestone details](https://img.shields.io/github/milestones/issues-open/lilytronics/lily-data-logger-studio-ce/1)](https://github.com/LilyTronics/lily-data-logger-studio-ce/milestone/1)

## Editions

The Lily Data Logger Studio has two editions:

### CE: Community Edition.

* Only for logging data (measurements).
* Provided as is and has no support.
* Free and open source.
* Build in driver for the following instruments:
  * Arduino DAQ: reading analog voltages, reading and writing digital IO, sketch for the Arduino is included in this repo and in the distribution package.
  * Multimeter simulator giving random values for voltage and current, for testing measurements.

### XE: eXtended Edition.

* All features of the CE.
* Process control automation:
  * Create and run processes to control your entire test setup (test automation).
  * Processes can contain:
    * setting values in instruments
    * process flow control depending on values read from instruments
    * loops for repeating process steps
    * wait statements for adding delays in the process
    * save and load processes from configuration files.
* Extra build-in drivers for the following instruments:
  * Tektronix oscilloscopes, using the serial port of the TDS2CM communications module.
    * TDS200 series: TDS210, TDS220, TDS224
    * TDS1000 series: TDS1001, TDS1002, TDS1012
    * TDS2000 series: TDS2002, TDS2004, TDS2012, TDS2014, TDS2022, TDS2024
  * TTi PL303QMD-P power supply, using the USB virtual COM port.
  * National Instruments USB-6009 DAQ, requires NI drivers, not included, installation manual available.
  * Protek 506 multimeter, using a USB to serial port converter.
  * Temperature chamber simulator, for testing the process control feature. 
* Support from LilyTronics.
  * Help when using the application and creating processes.
  * Help for adding your instruments.

The CE version is available through GitHub. The XE version is sold through our website at https://lilytronics.nl.

## Adding your own instruments

You can add your own instruments. A manual for that will be available on the first release.

## Development

Requirements for running the software:

* Python (>= 3.10)
* Upgrade pip: python -m pip install --upgrade pip
* pip install -r requirements.txt

In `tests` is a script for running the unit tests `run_unit_tests.py`
Test reports are written to `unit_test/test_reports`.

[![Pylint](https://github.com/LilyTronics/lily-data-logger-studio-ce/actions/workflows/pylint.yml/badge.svg?branch=main)](https://github.com/LilyTronics/lily-data-logger-studio-ce/actions/workflows/pylint.yml)
[![Documentation Status](https://readthedocs.org/projects/lily-data-logger-studio-ce/badge/?version=latest)](https://lily-data-logger-studio-ce.readthedocs.io/en/latest/?badge=latest)

2023 - LilyTronics (https://lilytronics.nl)
