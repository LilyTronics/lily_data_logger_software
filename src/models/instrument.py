"""
Instrument model.
"""

import json
import queue
import threading
import time


class Instrument:

    KEY_BAUD_RATE = "baud_rate"
    KEY_CHANNELS = "channels"
    KEY_COMMAND = "command"
    KEY_COMMAND_LIST = "command_list"
    KEY_INFO = "info"
    KEY_INITIALIZE = "initialize"
    KEY_INTERFACE = "interface"
    KEY_NAME = "name"
    KEY_RESPONSE = "response"
    KEY_SETTINGS = "settings"
    KEY_TYPE = "type"

    TYPE_INPUT = "input"
    TYPE_OUTPUT = "output"

    DEFAULT_NAME = "unknown"
    DEFAULT_INFO = "no info"

    BYTE_ENCODING = "latin"

    _TYPE_NAME_TO_TYPE = {
        b"float": float,
        b"int": int,
        b"str": str
    }

    _DEBUG_FORMAT = "{:20}: {}"

    def __init__(self, instrument_definition):
        self._instrument_definition = instrument_definition
        self._interface_object = None
        self._queue = queue.Queue()
        self._stop_event = threading.Event()
        self._queue_handler = None

    def __del__(self):
        self.stop()

    ###########
    # Private #
    ###########

    def _process_queue(self):
        while not self._stop_event.is_set():
            try:
                channel, value, callback, callback_id, debug = self._queue.get(True, 0.05)
                if self._interface_object is not None:
                    if debug:
                        print("Process request")
                        print(self._DEBUG_FORMAT.format("Channel data", channel))
                        print(self._DEBUG_FORMAT.format("Value", value))
                        print(self._DEBUG_FORMAT.format("Callback", callback))
                        print(self._DEBUG_FORMAT.format("Callback ID", callback_id))
                    response = self._process_commands(channel[self.KEY_COMMAND_LIST], value, debug)
                    callback(callback_id, response)

            except queue.Empty:
                pass

    def _get_channel(self, channel_type, channel_name):
        channel_data = self._instrument_definition.get(self.KEY_CHANNELS, [])
        matches = list(filter(lambda x: x[self.KEY_TYPE] == channel_type and
                              x[self.KEY_NAME] == channel_name, channel_data))
        assert len(matches) == 1, f"Channel '{channel_name}' of type {channel_type} not found"
        return matches[0]

    def _parse_mask(self, mask, debug):
        has_mask = False
        pre_response = b""
        post_response = b""
        value_type = b"str"
        x1 = mask.find(b"{")
        x2 = mask.find(b"}")
        if 0 <= x1 < x2:
            has_mask = True
            pre_response = mask[:x1]
            post_response = mask[x2 + 1:]
            value_type = mask[x1 + 1:x2]
        if debug:
            print("Parse mask:")
            print(self._DEBUG_FORMAT.format("Mask", mask))
            print(self._DEBUG_FORMAT.format("Has mask", has_mask))
            print(self._DEBUG_FORMAT.format("Pre response", pre_response))
            print(self._DEBUG_FORMAT.format("Post response", post_response))
            print(self._DEBUG_FORMAT.format("Value type", value_type))
        return has_mask, pre_response, post_response, value_type

    def _parse_response(self, expected_response, response, debug):
        if debug:
            print("Parsing response:")
            print(self._DEBUG_FORMAT.format("Expected response", expected_response))
            print(self._DEBUG_FORMAT.format("Response", response))
        response_data = self._parse_mask(expected_response, debug)
        if response_data[0]:
            if len(response_data[1]) > 0 and response.startswith(response_data[1]):
                response = response[len(response_data[1]):]
            if len(response_data[2]) > 0 and response.endswith(response_data[2]):
                response = response[:-len(response_data[2])]
            value = self._TYPE_NAME_TO_TYPE[response_data[3]](response.decode(self.BYTE_ENCODING))
        else:
            value = response.decode(self.BYTE_ENCODING)
        if debug:
            print(self._DEBUG_FORMAT.format("Value", f"({type(value)}) "
                                                     f"{str(value).encode(self.BYTE_ENCODING)}"))
        return value

    def _insert_value_in_command(self, command_mask, value, debug):
        format_string = "{}"
        command_data = self._parse_mask(command_mask, debug)
        if command_data[0]:
            parts = command_data[3].split(b":")
            value_type = parts[0]
            if value_type == b"float" and len(parts) > 1:
                format_string = f"{{:0.{int(parts[1])}f}}"
            if debug:
                print(self._DEBUG_FORMAT.format("Format string", format_string))
            command = command_data[1]
            command += format_string.format(self._TYPE_NAME_TO_TYPE[value_type](value)).encode(
                self.BYTE_ENCODING)
            command += command_data[2]
        else:
            command = command_mask
        return command

    def _execute_internal_command(self, command_data, debug):
        command = command_data[self.KEY_COMMAND].encode(self.BYTE_ENCODING)
        command_output = "Process internal command:\n"
        command_output += self._DEBUG_FORMAT.format("Command", command)
        if command.startswith(b"instrument_delay:"):
            delay = float(command.split(b":")[-1])
            if debug:
                print(command_output)
                print(self._DEBUG_FORMAT.format("Delay (s)", delay))
            time.sleep(delay)
            return True
        if command.startswith(b"interface:"):
            parts = command.split(b":")
            command = parts[1]
            param = None
            if len(parts) > 2:
                param = parts[2]
            if debug:
                print(command_output)
                print(self._DEBUG_FORMAT.format("Interface command", f"{command}, {param}"))
            if param is None:
                getattr(self._interface_object, command.decode(self.BYTE_ENCODING))()
            else:
                getattr(self._interface_object, command.decode(self.BYTE_ENCODING))(param)
            return True
        return False

    def _execute_interface_command(self, command_data, value, debug):
        pre_response = b""
        post_response = b""
        expected_response = b""
        command = command_data[self.KEY_COMMAND].encode(self.BYTE_ENCODING)
        if value is not None:
            command = self._insert_value_in_command(command, value, debug)
        if debug:
            print("Execute interface command:")
            print(self._DEBUG_FORMAT.format("Command", command))
        expect_response = self.KEY_RESPONSE in command_data.keys()
        if debug:
            print(self._DEBUG_FORMAT.format("Expect response", expect_response))
        if expect_response:
            expected_response = command_data[self.KEY_RESPONSE].encode(self.BYTE_ENCODING)
            response_data = self._parse_mask(expected_response, debug)
            if response_data[0]:
                pre_response = response_data[1]
                post_response = response_data[2]
            else:
                pre_response = post_response = expected_response
        if debug:
            print("Send interface command:")
            print(self._DEBUG_FORMAT.format("Command", command))
            print(self._DEBUG_FORMAT.format("Expect response", expect_response))
            print(self._DEBUG_FORMAT.format("Pre response", pre_response))
            print(self._DEBUG_FORMAT.format("Post response", post_response))
        response = self._interface_object.send_command(command, expect_response, pre_response,
                                                       post_response)
        if expect_response:
            response = self._parse_response(expected_response, response, debug)
        return response

    def _process_commands(self, command_list, value, debug):
        response = b""
        self._interface_object.acquire_lock()
        try:
            for command_data in command_list:
                if debug:
                    print("Process command:")
                    print(self._DEBUG_FORMAT.format("Command data", command_data))
                if not self._execute_internal_command(command_data, debug):
                    response = self._execute_interface_command(command_data, value, debug)
        finally:
            self._interface_object.release_lock()
        return response

    ##########
    # Public #
    ##########

    def start(self):
        if self._queue_handler is None or not self._queue_handler.is_alive():
            self._queue_handler = threading.Thread(target=self._process_queue)
            self._queue_handler.daemon = True
            self._stop_event.clear()
            self._queue_handler.start()

    def stop(self):
        if self._queue_handler is not None and self._queue_handler.is_alive():
            self._stop_event.set()
            self._queue_handler.join()
        self._queue_handler = None
        # Discard pending requests
        while True:
            try:
                self._queue.get_nowait()
            except queue.Empty:
                break

    def export_to_file(self, filename):
        output = {
            self.KEY_NAME: self.get_name(),
            self.KEY_INFO: self.get_info(),
            self.KEY_INTERFACE: self._instrument_definition.get(self.KEY_INTERFACE, {}),
            self.KEY_INITIALIZE: self._instrument_definition.get(self.KEY_INITIALIZE, []),
            self.KEY_CHANNELS: self._instrument_definition.get(self.KEY_CHANNELS, [])
        }
        with open(filename, "w", encoding="utf-8") as fp:
            json.dump(output, fp, indent=4)

    def get_name(self):
        return self._instrument_definition.get(self.KEY_NAME, self.DEFAULT_NAME)

    def get_info(self):
        return self._instrument_definition.get(self.KEY_INFO, self.DEFAULT_INFO)

    def get_interface_type(self):
        return self._instrument_definition.get(self.KEY_INTERFACE, {}).get(self.KEY_TYPE, None)

    def get_interface_settings(self):
        return self._instrument_definition.get(self.KEY_INTERFACE, {}).get(self.KEY_SETTINGS, {})

    def set_interface_object(self, interface_object):
        self._interface_object = interface_object

    def get_input_channels(self):
        channel_data = self._instrument_definition.get(self.KEY_CHANNELS, [])
        return list(filter(lambda x: x[self.KEY_TYPE] == self.TYPE_INPUT, channel_data))

    def initialize(self, debug=False):
        if debug:
            print("Initialize instrument")
        command_list = self._instrument_definition.get(self.KEY_INITIALIZE, [])
        if len(command_list) > 0:
            self._process_commands(command_list, None, debug)

    # pylint: disable=too-many-arguments
    def process_channel(self, channel_name, value=None, callback=None, callback_id=None,
                        debug=False):
        if value is None:
            channel = self._get_channel(self.TYPE_INPUT, channel_name)
        else:
            channel = self._get_channel(self.TYPE_OUTPUT, channel_name)
        response = None
        if callback is None or callback_id is None:
            if debug:
                print(self._DEBUG_FORMAT.format("Process channel", channel_name))
                print(self._DEBUG_FORMAT.format("Channel", channel))
            response = self._process_commands(channel[self.KEY_COMMAND_LIST], value, debug)
        else:
            if debug:
                print(self._DEBUG_FORMAT.format("Put request", channel_name))
            self._queue.put((channel, value, callback, callback_id, debug))
        return response


if __name__ == "__main__":

    import pylint
    from tests.unit_tests.test_models.test_instrument import TestInstrument

    TestInstrument().run(True)
    pylint.run_pylint([__file__])
