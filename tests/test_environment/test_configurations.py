"""
Test configurations containing various test configurations.
"""
from src.models.configuration import Configuration


class TestConfigurations:

    _CONFIGURATIONS = {}

    ##########
    # Public #
    ##########

    @classmethod
    def get_configuration_names(cls):
        return list(cls._CONFIGURATIONS)

    @classmethod
    def get_configuration(cls, name):
        return cls._CONFIGURATIONS.get(name, Configuration())

    @classmethod
    def init(cls):
        cls._CONFIGURATIONS["simple config"] = cls._create_simple()

    ###########
    # Private #
    ###########

    @classmethod
    def _create_simple(cls):
        conf = Configuration()
        conf.set_sample_time(2)
        conf.set_end_time(7)
        name = "Multimeter"
        settings = {
            conf.KEY_INSTRUMENT_NAME: "Simulator multimeter",
            conf.KEY_INSTRUMENT_SETTINGS: {
                "ip_address": "localhost",
                "ip_port": 17000,
                "rx_timeout": 0.2
            }
        }
        conf.update_instrument(name, name, settings)
        # We can only add a measurement if an instrument is added
        if len(conf.get_instruments()) > 0:
            instrument = conf.get_instruments()[0]
            name = "Current"
            settings = {
                conf.KEY_INSTRUMENT_ID: instrument[conf.KEY_ID],
                conf.KEY_MEASUREMENT: "Get DC current",
                conf.KEY_GAIN: 2.0,
                conf.KEY_OFFSET: 1.0
            }
            conf.update_measurement(name, name, settings)
        return conf


# Initialize the test configurations
TestConfigurations.init()


if __name__ == "__main__":

    import pylint

    for _name in TestConfigurations.get_configuration_names():
        print(_name, TestConfigurations.get_configuration(_name).__class__)

    pylint.run_pylint([__file__])
