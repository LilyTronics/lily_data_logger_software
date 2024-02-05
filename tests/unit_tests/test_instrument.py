"""
Test the instrument model.
"""

import os
import tempfile

from src.models.interfaces.interface import Interface
from src.models.instrument import Instrument
from tests.unit_tests.lib.test_suite import TestSuite


class TestInstrument(TestSuite):

    instrument_data = {
        "name": "Test instrument",
        "info": "Instrument for testing the model",
        "interface": {
            "type": "test interface"
        },
        "initialize": [
            {
                "command": "test init\n",
                "response": "OK\n"
            },
            {
                "command": "test init no response\n",
            },
            {
                "command": "instrument_delay:0.5"
            },
            {
                "command": "interface:custom_command:param"
            }
        ],
        "channels": [
            {
                "name": "get float",
                "type": "input",
                "command_list": [
                    {
                        "command": "get_float?\n",
                        "response": "voltage={float}V\n"
                    }
                ]
            },
            {
                "name": "get int",
                "type": "input",
                "command_list": [
                    {
                        "command": "get_int?\n",
                        "response": "count={int}\n"
                    }
                ]
            },
            {
                "name": "get str",
                "type": "input",
                "command_list": [
                    {
                        "command": "prepare_string\n",
                        "response": "OK\n"
                    },
                    {
                        "command": "instrument_delay:0.5",
                    },
                    {
                        "command": "get_str?\n",
                        "response": "name={str}\n"
                    }
                ]
            },
            {
                "name": "set float 1",
                "type": "output",
                "command_list": [
                    {
                        "command": "voltage={float}\n",
                        "response": "OK\n"
                    }
                ]
            },
            {
                "name": "set float 2",
                "type": "output",
                "command_list": [
                    {
                        "command": "voltage={float:2}\n",
                        "response": "OK\n"
                    }
                ]
            },
            {
                "name": "set int",
                "type": "output",
                "command_list": [
                    {
                        "command": "state={int}\n",
                        "response": "OK\n"
                    }
                ]
            },
            {
                "name": "set str",
                "type": "output",
                "command_list": [
                    {
                        "command": "instrument_delay:0.5",
                    },
                    {
                        "command": "label={str}\n",
                        "response": "OK\n"
                    }
                ]
            },
            {
                "name": "set no response",
                "type": "output",
                "command_list": [
                    {
                        "command": "label={str}\n",
                    }
                ]
            }
        ]
    }

    def _create_instrument(self):
        instrument = Instrument(self.instrument_data)
        interface = TestInterface()
        instrument.set_interface_object(interface)
        return instrument

    def test_default_values(self):
        instrument = Instrument({})
        self.log.debug("Check default name")
        self.fail_if(instrument.get_name() != instrument.DEFAULT_NAME,
                     "The default name is not correct '{}'".format(instrument.get_name()))
        self.log.debug("Check default info")
        self.fail_if(instrument.get_info() != instrument.DEFAULT_INFO,
                     "The default info is not correct '{}'".format(instrument.get_info()))
        self.log.debug("Check default interface type")
        self.fail_if(instrument.get_interface_type() is not None,
                     "The default interface type is not correct '{}'".format(instrument.get_interface_type()))
        self.log.debug("Check default interface settings")
        self.fail_if(instrument.get_interface_settings() != {},
                     "The default interface settings is not correct '{}'".format(instrument.get_interface_settings()))

    def test_instrument_data(self):
        instrument = Instrument(self.instrument_data)
        self.log.debug("Check name")
        self.fail_if(instrument.get_name() != "Test instrument",
                     "The name is not correct '{}'".format(instrument.get_name()))
        self.log.debug("Check info")
        self.fail_if(instrument.get_info() != "Instrument for testing the model",
                     "The info is not correct '{}'".format(instrument.get_name()))
        self.log.debug("Check interface")
        self.fail_if(instrument.get_interface_type() != "test interface",
                     "The interface type is not correct '{}'".format(instrument.get_interface_type()))

    def test_float_input(self):
        instrument = self._create_instrument()
        self.log.debug("Test float input")
        value = instrument.get_value("get float")
        self.fail_if(type(value) is not float, "Value is not type float")
        self.fail_if(value != 5.03, "Value is not correct")

    def test_int_input(self):
        instrument = self._create_instrument()
        self.log.debug("Test int input")
        value = instrument.get_value("get int")
        self.fail_if(type(value) is not int, "Value is not type int")
        self.fail_if(value != 12, "Value is not correct")

    def test_str_input(self):
        instrument = self._create_instrument()
        self.log.debug("Test str input")
        value = instrument.get_value("get str")
        self.fail_if(type(value) is not str, "Value is not type str")
        self.fail_if(value != "test instrument", "Value is not correct")

    def test_float_output(self):
        instrument = self._create_instrument()
        self.log.debug("Test float 1 output")
        response = instrument.set_value("set float 1", "5")
        self.fail_if(response != "OK\n", "The response is not correct")
        self.log.debug("Test float 2 output")
        response = instrument.set_value("set float 2", "8")
        self.fail_if(response != "OK\n", "The response is not correct")

    def test_int_output(self):
        instrument = self._create_instrument()
        self.log.debug("Test int output")
        response = instrument.set_value("set int", "7")
        self.fail_if(response != "OK\n", "The response is not correct")

    def test_str_output(self):
        instrument = self._create_instrument()
        self.log.debug("Test str output")
        response = instrument.set_value("set str", "test output")
        self.fail_if(response != "OK\n", "The response is not correct")

    def test_no_response(self):
        instrument = self._create_instrument()
        self.log.debug("Test command with no response")
        response = instrument.set_value("set no response", "no response")
        self.fail_if(response != b"", "The response is not correct")

    def test_initialize(self):
        instrument = self._create_instrument()
        instrument.initialize()

    def test_export_to_file(self):
        instrument = self._create_instrument()
        path = os.path.join(tempfile.gettempdir(), "test_instrument.json")
        instrument.export_to_file(path)

    def test_get_inputs(self):
        instrument = self._create_instrument()
        channels = instrument.get_input_channels()
        self.fail_if(len(channels) != 3, "Did get the correct number of input channels")


class TestInterface(Interface):

    _COMMAND_TO_RESPONSE = {
        b"get_float?\n": b"voltage=5.03V\n",
        b"get_int?\n": b"count=12\n",
        b"prepare_string\n": b"OK\n",
        b"get_str?\n": b"name=test instrument\n",
        b"voltage=5.0\n": b"OK\n",
        b"voltage=8.00\n": b"OK\n",
        b"state=7\n": b"OK\n",
        b"label=test output\n": b"OK\n",
        b"label=no response\n": b"",
        b"test init\n": b"OK\n",
        b"test init no response\n": b""
    }

    def send_command(self, command, expect_response=True):
        assert command in self._COMMAND_TO_RESPONSE.keys(), "Unknown command '{}'".format(command)
        if expect_response:
            return self._COMMAND_TO_RESPONSE[command]
        return b""

    @staticmethod
    def custom_command(param):
        print("Custom command with param {}".format(param))


if __name__ == "__main__":

    TestInstrument().run()
