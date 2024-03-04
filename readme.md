# Lily Data Logger Studio CE (Community Edition)

Universal data logger software aiming to work with any kind of electronics measurement device (mulitmeters, oscilloscopes, power supplies, etc.).

![main view](docs/images/main_view.png)

## Releases

Coming up V1.0.0:

[![GitHub milestone details](https://img.shields.io/github/milestones/issues-open/lilytronics/lily-data-logger-studio-ce/1)](https://github.com/LilyTronics/lily-data-logger-studio-ce/milestone/1)

## Features

* Only for logging data (measurements).
* Provided as is and has no support.
* Free and open source.
* Build in driver for the following instruments:
  * Arduino DAQ: reading analog voltages, reading and writing digital IO, sketch for the Arduino is included in this repo and in the distribution package.
  * Multimeter simulator giving random values for voltage and current, for testing measurements.

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
