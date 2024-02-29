"""
Test configurations containing various test configurations.
"""

from src.models.configuration import Configuration
from src.simulators.simulator_settings import SimulatorSettings


class TestConfigurations:

    _CONFIGURATIONS = {}

    ##########
    # Public #
    ##########

    @classmethod
    def init(cls):
        cls._CONFIGURATIONS["all simulators, 2s/7s"] = cls._create_all_simulators(2, 7)
        cls._CONFIGURATIONS["all simulators, 2s/5m"] = cls._create_all_simulators(2, 300)

    @classmethod
    def get_configuration_names(cls):
        return list(cls._CONFIGURATIONS)

    @classmethod
    def get_configuration(cls, name):
        return cls._CONFIGURATIONS.get(name, Configuration())

    @classmethod
    def get_unit_test_configuration(cls):
        return cls.get_configuration("all simulators, 2s/7s")

    ###########
    # Private #
    ###########

    @classmethod
    def _create_all_simulators(cls, sample_time, duration):
        conf = Configuration()
        conf.set_sample_time(sample_time)
        conf.set_end_time(duration)
        cls._add_multimeter(conf)
        cls._add_temperature_meter(conf)
        return conf

    @staticmethod
    def _add_multimeter(conf):
        name = "Multimeter"
        settings = {
            conf.KEY_INSTRUMENT_NAME: "Simulator multimeter",
            conf.KEY_INSTRUMENT_SETTINGS: {
                "ip_address": SimulatorSettings.MultimeterUdp.IP,
                "ip_port": SimulatorSettings.MultimeterUdp.PORT,
                "rx_timeout": SimulatorSettings.MultimeterUdp.RX_TIME_OUT
            }
        }
        conf.update_instrument(name, name, settings)
        if len(conf.get_instruments()) > 0:
            for measurement in (("Volt", "Get DC voltage"), ("Curr", "Get DC current")):
                instrument = conf.get_instrument("Multimeter")
                settings = {
                    conf.KEY_INSTRUMENT_ID: instrument[conf.KEY_ID],
                    conf.KEY_MEASUREMENT: measurement[1],
                    conf.KEY_GAIN: 1.0,
                    conf.KEY_OFFSET: 0.0
                }
                conf.update_measurement(measurement[0], measurement[0], settings)
        return conf

    @staticmethod
    def _add_temperature_meter(conf):
        name = "Temperature meter"
        settings = {
            conf.KEY_INSTRUMENT_NAME: "Simulator temperature meter",
            conf.KEY_INSTRUMENT_SETTINGS: {
                "ip_address": SimulatorSettings.TemperatureMeterTcp.IP,
                "ip_port": SimulatorSettings.TemperatureMeterTcp.PORT,
                "rx_timeout": SimulatorSettings.TemperatureMeterTcp.RX_TIME_OUT
            }
        }
        conf.update_instrument(name, name, settings)
        if len(conf.get_instruments()) > 0:
            instrument = conf.get_instrument("Temperature meter")
            settings = {
                conf.KEY_INSTRUMENT_ID: instrument[conf.KEY_ID],
                conf.KEY_MEASUREMENT: "Get temperature",
                conf.KEY_GAIN: 1.0,
                conf.KEY_OFFSET: 0.0
            }
            conf.update_measurement("Outside temperature", "Outside temperature", settings)
        return conf


# Initialize the test configurations
TestConfigurations.init()


if __name__ == "__main__":

    import pylint

    for _name in TestConfigurations.get_configuration_names():
        print(_name, TestConfigurations.get_configuration(_name).__class__)

    pylint.run_pylint([__file__])
