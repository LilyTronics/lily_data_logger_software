"""
Instrument model.
"""

import lily_unit_test

from src.models.interfaces.interface import Interface


class Instrument(object):

    KEY_BAUD_RATE = 'baud_rate'
    KEY_CHANNELS = 'channels'
    KEY_COMMAND = 'command'
    KEY_INFO = 'info'
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

    def __init__(self, instrument_definition):
        self._name = instrument_definition.get(self.KEY_NAME, self.DEFAULT_NAME)
        self._info = instrument_definition.get(self.KEY_INFO, self.DEFAULT_INFO)
        self._interface_data = instrument_definition.get(self.KEY_INTERFACE, {})
        self._channel_data = instrument_definition.get(self.KEY_CHANNELS, {})
        self._interface_object = None

    ###########
    # Private #
    ###########

    def _get_channel(self, channel_type, channel_name):
        matches = list(filter(lambda x: x[self.KEY_TYPE] == channel_type and x[self.KEY_NAME] == channel_name,
                              self._channel_data))
        assert len(matches) == 1, 'Channel {} of type {} not found'.format(channel_name, channel_type)
        return matches[0]

    def _get_value(self, channel_name):
        pre_response = b''
        post_response = b''
        value_type = b'str'

        channel = self._get_channel(self.TYPE_INPUT, channel_name)
        response_mask = channel[self.KEY_RESPONSE].encode(self.BYTE_ENCODING)
        x1 = response_mask.find(b'{')
        x2 = response_mask.find(b'}')
        if x1 >= 0 and x2 >= 0:
            pre_response = response_mask[:x1]
            post_response = response_mask[x2 + 1:]
            value_type = response_mask[x1 + 1:x2].split(b':')[0]
        response = self._interface_object.send_command(channel[self.KEY_COMMAND].encode(self.BYTE_ENCODING))
        if len(pre_response) > 0 and response.startswith(pre_response):
            response = response[len(pre_response):]
        if len(post_response) > 0 and response.endswith(post_response):
            response = response[:-len(post_response)]
        return self._TYPE_NAME_TO_TYPE[value_type](response)

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

    def get_value(self, channel_name):
        return self._get_value(channel_name)

    def set_value(self, channel_name, value):
        pass


class TestInstrument(lily_unit_test.TestSuite):

    instrument_data = {
        'name': 'Test instrument',
        'info': 'Instrument for testing the model',
        'interface': {
            'type': 'test interface'
        },
        'channels': [
            {
                'name': 'get float',
                'type': 'input',
                'command': 'get_float?\n',
                'response': 'voltage={float}V\n'
            }
        ]
    }

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

    def test_inputs(self):
        instrument = Instrument(self.instrument_data)
        interface = TestInterface()
        instrument.set_interface_object(interface)
        self.log.debug('Test float input')
        value = instrument.get_value('get float')
        self.fail_if(type(value) is not float, 'Value is not type float')
        self.fail_if(value != 5.03, 'Value is not correct')


class TestInterface(Interface):

    _COMMAND_TO_RESPONSE = {
        b'get_float?\n': b'voltage=5.03V\n'
    }

    def send_command(self, command):
        return self._COMMAND_TO_RESPONSE[command]


if __name__ == '__main__':

    TestInstrument().run(True)
