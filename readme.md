# Lily Data Logger Studio CE (Community Edition)

Universal data logger software aiming to work with any kind of electronics measurement device.

## Releases

Comming up V1.0.0:

[![GitHub milestone details](https://img.shields.io/github/milestones/issues-open/lilytronics/lily-data-logger-studio-ce/1)](https://github.com/LilyTronics/lily-data-logger-studio-ce/milestone/1)

## Editions

The Lily Data Logger Studio has two editions:

* CE: Community Edition.
  * Only for logging data (measurements).
  * Provided as is and has no support.
  * Free and open source.


* XE: eXtended Edition.
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
    * Tektronics TD220 (or similar: TDS200/TDS1000/TDS2000).
    * TTi PL303QMD-P power supply.
    * National Instruments USB-6009 DAQ (requires NI drivers, not included, installation manual available).
    * Protek 506 multimeter.
    * Temperature chamber simulator (for testing the process control feature). 
  * Support from LilyTronics.
    * Help when using the application and creating processes.
    * Help for adding your instruments.

The CE version is available through GitHub. The XE version is sold through our website at https://lilytronics.nl.

## Instruments

The following instruments are included in the application:
* Arduino DAQ: reading analog voltages, reading and writing digital IO, sketch for the Arduino is included in this repo.
* Simulators (for testing/demo):
  * Multimeter giving random values for voltage and current

## Adding your own instruments

You can add your own instruments. A manual for that will be available on the first release.

## Development

Requirements for running the software:

* Python (>= 3.10)
* Upgrade pip: python -m pip install --upgrade pip
* pip install -r requirements.txt

In `tests` is a script for running the unit tests `run_unit_tests.py`
Test reports are written to `unit_test/test_reports`.

2023 - LilyTronics (https://lilytronics.nl)
