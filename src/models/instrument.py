"""
Instrument model.
"""

import time

from src.models.interfaces.interface import Interface
from unit_test.test_suite import TestSuite


class Instrument(object):

    KEY_BAUD_RATE = 'baud_rate'
    KEY_CHANNELS = 'channels'
    KEY_COMMAND = 'command'
    KEY_COMMAND_LIST = 'command_list'
    KEY_INFO = 'info'
    KEY_INITIALIZE = 'initialize'
    KEY_INTERFACE = 'interface'
    KEY_NAME = 'name'
    KEY_RESPONSE = 'response'
    KEY_SETTINGS = 'settings'
    KEY_TYPE = 'type'

    TYPE_INPUT = 'input'
    TYPE_OUTPUT = 'output'

    DEFAULT_NAME = 'unknown'
    DEFAULT_INFO = 'no info'

    BYTE_ENCODING = 'latin'

    _TYPE_NAME_TO_TYPE = {
        b'float': float,
        b'int': int,
        b'str': str
    }

    _DEBUG_FORMAT = '{:18}: {}'

    def __init__(self, instrument_definition):
        self._name = instrument_definition.get(self.KEY_NAME, self.DEFAULT_NAME)
        self._info = instrument_definition.get(self.KEY_INFO, self.DEFAULT_INFO)
        self._interface_data = instrument_definition.get(self.KEY_INTERFACE, {})
        self._initialize_data = instrument_definition.get(self.KEY_INITIALIZE, [])
        self._channel_data = instrument_definition.get(self.KEY_CHANNELS, [])
        self._interface_object = None

    ###########
    # Private #
    ###########

    def _get_channel(self, channel_type, channel_name):
        matches = list(filter(lambda x: x[self.KEY_TYPE] == channel_type and x[self.KEY_NAME] == channel_name,
                              self._channel_data))
        assert len(matches) == 1, 'Channel {} of type {} not found'.format(channel_name, channel_type)
        return matches[0]

    @staticmethod
    def _parse_mask(mask):
        has_mask = False
        pre_response = b''
        post_response = b''
        value_type = b'str'
        x1 = mask.find(b'{')
        x2 = mask.find(b'}')
        if 0 <= x1 < x2:
            has_mask = True
            pre_response = mask[:x1]
            post_response = mask[x2 + 1:]
            value_type = mask[x1 + 1:x2]
        return has_mask, pre_response, post_response, value_type

    def _parse_response(self, expected_response, response, debug):
        if debug:
            print(self._DEBUG_FORMAT.format('Expected response', expected_response))
            print(self._DEBUG_FORMAT.format('Response', response))
        response_data = self._parse_mask(expected_response)
        if debug:
            print(self._DEBUG_FORMAT.format('Has mask', response_data[0]))
            print(self._DEBUG_FORMAT.format('Pre response', response_data[1]))
            print(self._DEBUG_FORMAT.format('Post response', response_data[2]))
            print(self._DEBUG_FORMAT.format('Value type', response_data[3]))
        if response_data[0]:
            if len(response_data[1]) > 0 and response.startswith(response_data[1]):
                response = response[len(response_data[1]):]
            if len(response_data[2]) > 0 and response.endswith(response_data[2]):
                response = response[:-len(response_data[2])]
            value = self._TYPE_NAME_TO_TYPE[response_data[3]](response.decode(self.BYTE_ENCODING))
        else:
            value = response.decode(self.BYTE_ENCODING)
        if debug:
            print(self._DEBUG_FORMAT.format('Value', '({}) {}'.format(
                type(value), str(value).encode(self.BYTE_ENCODING))))
        return value

    def _insert_value_in_command(self, command_mask, value, debug):
        format_string = '{}'
        command_data = self._parse_mask(command_mask)
        if debug:
            print(self._DEBUG_FORMAT.format('Command mask', command_mask))
            print(self._DEBUG_FORMAT.format('Has mask', command_data[0]))
            print(self._DEBUG_FORMAT.format('Pre response', command_data[1]))
            print(self._DEBUG_FORMAT.format('Post response', command_data[2]))
            print(self._DEBUG_FORMAT.format('Value type', command_data[3]))
        if command_data[0]:
            parts = command_data[3].split(b':')
            value_type = parts[0]
            if value_type == b'float' and len(parts) > 1:
                format_string = '{{:0.{}f}}'.format(int(parts[1]))
            if debug:
                print(self._DEBUG_FORMAT.format('Format string', format_string))
            command = command_data[1]
            command += format_string.format(self._TYPE_NAME_TO_TYPE[value_type](value)).encode(self.BYTE_ENCODING)
            command += command_data[2]
        else:
            command = command_mask
        return command

    def _execute_internal_command(self, command, debug):
        if command.startswith(b'instrument_delay:'):
            delay = float(command.split(b':')[-1])
            if debug:
                print(self._DEBUG_FORMAT.format('Delay (s)', delay))
            time.sleep(delay)
            return True
        return False

    def _process_command(self, command_data, debug, value=None):
        if debug:
            print(self._DEBUG_FORMAT.format('Command data', command_data))
        response = b''
        command = command_data[self.KEY_COMMAND].encode(self.BYTE_ENCODING)
        if value is not None:
            command = self._insert_value_in_command(command, value, debug)
        if debug:
            print(self._DEBUG_FORMAT.format('Command', command))
        if not self._execute_internal_command(command, debug):
            expect_response = self.KEY_RESPONSE in command_data.keys()
            response = self._interface_object.send_command(command, expect_response)
            if expect_response:
                expected_response = command_data[self.KEY_RESPONSE].encode(self.BYTE_ENCODING)
                response = self._parse_response(expected_response, response, debug)

        return response

    ##########
    # Public #
    ##########

    def get_name(self):
        return self._name

    def get_info(self):
        return self._info

    def get_interface_type(self):
        return self._interface_data.get(self.KEY_TYPE, None)

    def get_interface_settings(self):
        return self._interface_data.get(self.KEY_SETTINGS, {})

    def set_interface_object(self, interface_object):
        self._interface_object = interface_object

    def initialize(self, debug=False):
        if debug:
            print('Initialize instrument')
        for command_data in self._initialize_data:
            response = self._process_command(command_data, debug)
            if self.KEY_RESPONSE in command_data.keys():
                assert response == command_data[self.KEY_RESPONSE], 'Initialize command {} failed {}'.format(
                    command_data[self.KEY_COMMAND], command_data[self.KEY_RESPONSE])

    def get_value(self, channel_name, debug=False):
        if debug:
            print('<{}>.get_value( \'{}\' )'.format(self.get_name(), channel_name))
        channel = self._get_channel(self.TYPE_INPUT, channel_name)
        if debug:
            print(self._DEBUG_FORMAT.format('Channel', channel))
        response = None
        for command_data in channel[self.KEY_COMMAND_LIST]:
            response = self._process_command(command_data, debug)
        return response

    def set_value(self, channel_name, value, debug=False):
        if debug:
            print('DEBUG: <{}>.set_value( \'{}\', {} )'.format(self.get_name(), channel_name, value))
        channel = self._get_channel(self.TYPE_OUTPUT, channel_name)
        if debug:
            print(self._DEBUG_FORMAT.format('Channel', channel))
        response = None
        for command_data in channel[self.KEY_COMMAND_LIST]:
            response = self._process_command(command_data, debug, value)
        return response


class TestInstrument(TestSuite):

    instrument_data = {
        'name': 'Test instrument',
        'info': 'Instrument for testing the model',
        'interface': {
            'type': 'test interface'
        },
        'initialize': [
            {
                'command': 'test init\n',
                'response': 'OK\n'
            },
            {
                'command': 'instrument_delay:0.5'
            },
            {
                'command': 'test init no response\n',
            }
        ],
        'channels': [
            {
                'name': 'get float',
                'type': 'input',
                'command_list': [
                    {
                        'command': 'get_float?\n',
                        'response': 'voltage={float}V\n'
                    }
                ]
            },
            {
                'name': 'get int',
                'type': 'input',
                'command_list': [
                    {
                        'command': 'get_int?\n',
                        'response': 'count={int}\n'
                    }
                ]
            },
            {
                'name': 'get str',
                'type': 'input',
                'command_list': [
                    {
                        'command': 'prepare_string\n',
                        'response': 'OK\n'
                    },
                    {
                        'command': 'instrument_delay:0.5',
                    },
                    {
                        'command': 'get_str?\n',
                        'response': 'name={str}\n'
                    }
                ]
            },
            {
                'name': 'set float 1',
                'type': 'output',
                'command_list': [
                    {
                        'command': 'voltage={float}\n',
                        'response': 'OK\n'
                    }
                ]
            },
            {
                'name': 'set float 2',
                'type': 'output',
                'command_list': [
                    {
                        'command': 'voltage={float:2}\n',
                        'response': 'OK\n'
                    }
                ]
            },
            {
                'name': 'set int',
                'type': 'output',
                'command_list': [
                    {
                        'command': 'state={int}\n',
                        'response': 'OK\n'
                    }
                ]
            },
            {
                'name': 'set str',
                'type': 'output',
                'command_list': [
                    {
                        'command': 'instrument_delay:0.5',
                    },
                    {
                        'command': 'label={str}\n',
                        'response': 'OK\n'
                    }
                ]
            },
            {
                'name': 'set no response',
                'type': 'output',
                'command_list': [
                    {
                        'command': 'label={str}\n',
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
        self.log.debug('Check default name')
        self.fail_if(instrument.get_name() != instrument.DEFAULT_NAME,
                     'The default name is not correct {}'.format(instrument.get_name()))
        self.log.debug('Check default info')
        self.fail_if(instrument.get_info() != instrument.DEFAULT_INFO,
                     'The default info is not correct {}'.format(instrument.get_info()))
        self.log.debug('Check default interface type')
        self.fail_if(instrument.get_interface_type() is not None,
                     'The default interface type is not correct {}'.format(instrument.get_interface_type()))
        self.log.debug('Check default interface settings')
        self.fail_if(instrument.get_interface_settings() != {},
                     'The default interface settings is not correct {}'.format(instrument.get_interface_settings()))

    def test_instrument_data(self):
        instrument = Instrument(self.instrument_data)
        self.log.debug('Check name')
        self.fail_if(instrument.get_name() != 'Test instrument',
                     'The name is not correct {}'.format(instrument.get_name()))
        self.log.debug('Check info')
        self.fail_if(instrument.get_info() != 'Instrument for testing the model',
                     'The info is not correct {}'.format(instrument.get_name()))
        self.log.debug('Check interface')
        self.fail_if(instrument.get_interface_type() != 'test interface',
                     'The interface type is not correct {}'.format(instrument.get_interface_type()))

    def test_float_input(self):
        instrument = self._create_instrument()
        self.log.debug('Test float input')
        value = instrument.get_value('get float')
        self.fail_if(type(value) is not float, 'Value is not type float')
        self.fail_if(value != 5.03, 'Value is not correct')

    def test_int_input(self):
        instrument = self._create_instrument()
        self.log.debug('Test int input')
        value = instrument.get_value('get int')
        self.fail_if(type(value) is not int, 'Value is not type int')
        self.fail_if(value != 12, 'Value is not correct')

    def test_str_input(self):
        instrument = self._create_instrument()
        self.log.debug('Test str input')
        value = instrument.get_value('get str')
        self.fail_if(type(value) is not str, 'Value is not type str')
        self.fail_if(value != 'test instrument', 'Value is not correct')

    def test_float_output(self):
        instrument = self._create_instrument()
        self.log.debug('Test float 1 output')
        response = instrument.set_value('set float 1', '5')
        self.fail_if(response != 'OK\n', 'The response is not correct')
        self.log.debug('Test float 2 output')
        response = instrument.set_value('set float 2', '8')
        self.fail_if(response != 'OK\n', 'The response is not correct')

    def test_int_output(self):
        instrument = self._create_instrument()
        self.log.debug('Test int output')
        response = instrument.set_value('set int', '7')
        self.fail_if(response != 'OK\n', 'The response is not correct')

    def test_str_output(self):
        instrument = self._create_instrument()
        self.log.debug('Test str output')
        response = instrument.set_value('set str', 'test output')
        self.fail_if(response != 'OK\n', 'The response is not correct')

    def test_no_response(self):
        instrument = self._create_instrument()
        self.log.debug('Test command with no response')
        response = instrument.set_value('set no response', 'no response')
        self.fail_if(response != b'', 'The response is not correct')

    def test_initialize(self):
        instrument = self._create_instrument()
        instrument.initialize()


class TestInterface(Interface):

    _COMMAND_TO_RESPONSE = {
        b'get_float?\n': b'voltage=5.03V\n',
        b'get_int?\n': b'count=12\n',
        b'prepare_string\n': b'OK\n',
        b'get_str?\n': b'name=test instrument\n',
        b'voltage=5.0\n': b'OK\n',
        b'voltage=8.00\n': b'OK\n',
        b'state=7\n': b'OK\n',
        b'label=test output\n': b'OK\n',
        b'label=no response\n': b'',
        b'test init\n': b'OK\n',
        b'test init no response\n': b''
    }

    def send_command(self, command, expect_response=True):
        assert command in self._COMMAND_TO_RESPONSE.keys(), 'Unknown command {}'.format(command)
        if expect_response:
            return self._COMMAND_TO_RESPONSE[command]
        return b''


if __name__ == '__main__':

    TestInstrument().run()
