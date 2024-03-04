# Lily Data Logger Studio CE (Community Edition)

Universal data logger software aiming to work with any kind of electronics measurement device (mulitmeters, oscilloscopes, power supplies, etc.).

![main view](docs/images/main_view.png)

## Releases

Coming up V1.0.0:

[![GitHub milestone details](https://img.shields.io/github/milestones/issues-open/lilytronics/lily-data-logger-studio-ce/1)](https://github.com/LilyTronics/lily-data-logger-studio-ce/milestone/1)

## Features

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

## Adding your own instruments

You can add your own instruments. A manual for that will be available on the first release.

## Development

Requirements for running the software:

* Python (>= 3.10)
* Upgrade pip: python -m pip install --upgrade pip
* pip install -r requirements.txt

In `tests` is are several scripts for running the unit tests.
Test reports are written to `unit_test/test_reports`.

[![Pylint](https://github.com/LilyTronics/lily-data-logger-studio-ce/actions/workflows/pylint.yml/badge.svg?branch=main)](https://github.com/LilyTronics/lily-data-logger-studio-ce/actions/workflows/pylint.yml)
[![Documentation Status](https://readthedocs.org/projects/lily-data-logger-studio-ce/badge/?version=latest)](https://lily-data-logger-studio-ce.readthedocs.io/en/latest/?badge=latest)

2023 - LilyTronics (https://lilytronics.nl)
