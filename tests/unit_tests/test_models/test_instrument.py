"""
Test the instrument model.
"""

import os
import tempfile

from src.models.interfaces.interface import Interface
from src.models.instrument import Instrument
from tests.unit_tests.lib.test_suite import TestSuite


class TestInstrument(TestSuite):

    _instrument = None
    _callback_received = [False]

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

    def setup(self):
        self._instrument = Instrument(self.instrument_data)
        interface = TestInterface()
        self._instrument.set_interface_object(interface)
        self._instrument.start()

    def test_default_values(self):
        instrument = Instrument({})
        self.log.debug("Check default name")
        self.fail_if(instrument.get_name() != instrument.DEFAULT_NAME,
                     f"The default name is not correct '{instrument.get_name()}'")
        self.log.debug("Check default info")
        self.fail_if(instrument.get_info() != instrument.DEFAULT_INFO,
                     f"The default info is not correct '{instrument.get_info()}'")
        self.log.debug("Check default interface type")
        self.fail_if(instrument.get_interface_type() is not None,
                     "The default interface type is not correct "
                     f"'{self._instrument.get_interface_type()}'")
        self.log.debug("Check default interface settings")
        self.fail_if(instrument.get_interface_settings() != {},
                     "The default interface settings is not correct "
                     f"'{self._instrument.get_interface_settings()}'")

    def test_instrument_data(self):
        self.log.debug("Check name")
        self.fail_if(self._instrument.get_name() != "Test instrument",
                     f"The name is not correct '{self._instrument.get_name()}'")
        self.log.debug("Check info")
        self.fail_if(self._instrument.get_info() != "Instrument for testing the model",
                     f"The info is not correct '{self._instrument.get_name()}'")
        self.log.debug("Check interface")
        self.fail_if(self._instrument.get_interface_type() != "test interface",
                     f"The interface type is not correct '{self._instrument.get_interface_type()}'")

    def test_float_input(self):
        self.log.debug("Test float input")
        value = self._instrument.process_channel("get float")
        self.fail_if(not isinstance(value, float), "Value is not type float")
        self.fail_if(value != 5.03, "Value is not correct")

    def test_int_input(self):
        self.log.debug("Test int input")
        value = self._instrument.process_channel("get int")
        self.fail_if(not isinstance(value, int), "Value is not type int")
        self.fail_if(value != 12, "Value is not correct")

    def test_str_input(self):
        self.log.debug("Test str input")
        value = self._instrument.process_channel("get str")
        self.fail_if(not isinstance(value, str), "Value is not type str")
        self.fail_if(value != "test instrument", "Value is not correct")

    def test_float_output(self):
        self.log.debug("Test float 1 output")
        response = self._instrument.process_channel("set float 1", "5")
        self.fail_if(response != "OK\n", "The response is not correct")
        self.log.debug("Test float 2 output")
        response = self._instrument.process_channel("set float 2", "8")
        self.fail_if(response != "OK\n", "The response is not correct")

    def test_int_output(self):
        self.log.debug("Test int output")
        response = self._instrument.process_channel("set int", "7")
        self.fail_if(response != "OK\n", "The response is not correct")

    def test_str_output(self):
        self.log.debug("Test str output")
        response = self._instrument.process_channel("set str", "test output")
        self.fail_if(response != "OK\n", "The response is not correct")

    def test_no_response(self):
        self.log.debug("Test command with no response")
        response = self._instrument.process_channel("set no response", "no response")
        self.fail_if(response != b"", "The response is not correct")

    def test_initialize(self):
        self._instrument.initialize()

    def test_export_to_file(self):
        path = os.path.join(tempfile.gettempdir(), "test_instrument.json")
        self._instrument.export_to_file(path)

    def test_get_inputs(self):
        channels = self._instrument.get_input_channels()
        self.fail_if(len(channels) != 3, "Did get the correct number of input channels")

    def test_request_queue(self):
        def _callback(*args):
            self._callback_received[0] = True
            self._callback_received.append(args)

        self._callback_received[0] = False
        self.log.debug("Test str input by using the request queue")
        self._instrument.process_channel("get str", None, _callback, 1)
        if not self.wait_for(self._callback_received, True, 2, 0.1):
            self.fail("No callback received")
        callback_id, response = self._callback_received[1]
        self.fail_if(callback_id != 1, f"Wrong callback ID: {callback_id}")
        self.fail_if(response != "test instrument", f"Wrong response: '{response}'")

    def teardown(self):
        self._instrument.stop()


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

    def __init__(self):
        super().__init__({})

    def send_command(self, command, expect_response=True, pre_response=b"", post_response=b""):
        assert command in self._COMMAND_TO_RESPONSE, f"Unknown command '{command}'"
        if expect_response and (pre_response != b"" or post_response != b""):
            response = self._COMMAND_TO_RESPONSE[command]
            if response.startswith(pre_response) and response.endswith(post_response):
                return response
        return b""

    @staticmethod
    def custom_command(param):
        print(f"Custom command with param {param}")

    def is_open(self):
        return True

    def open(self):
        pass

    def close(self):
        pass

    @classmethod
    def get_settings_controls(cls):
        pass


if __name__ == "__main__":

    TestInstrument().run(True)
