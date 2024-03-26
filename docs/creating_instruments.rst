Creating your own instruments
=============================

It is impossible to have all instruments supported out of the box. Therefore there is a way to add
your own instruments.

The instruments can be added by creating a JSOn formatted file that defines all the measurements for
an instrument.

The instrument must comply to the following specifications:

* The communication protocol must be using ASCII characters.
* The interface should be serial, UDP or TCP.
* There must not be a user login procedure for the instrument (no authentication needed).



