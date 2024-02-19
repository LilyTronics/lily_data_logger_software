"""
Generates various test configurations for testing.
"""

from src.models.configuration import Configuration


class TestConfiguration(Configuration):

    def __init__(self, add_instrument=False, add_measurement=False):
        super().__init__()
        self.set_sample_time(2)
        self.set_end_time(7)
        if add_instrument:
            name = "Test instrument"
            settings = {
                self.KEY_INSTRUMENT_NAME: "Simulator multimeter",
                self.KEY_INSTRUMENT_SETTINGS: {
                    "ip_address": "localhost",
                    "ip_port": 17000,
                    "rx_timeout": 0.2
                }
            }
            self.update_instrument(name, name, settings)
        # We can only add a measurement if an instrument is added
        if add_measurement and len(self.get_instruments()) > 0:
            instrument = self.get_instruments()[0]
            name = "Current"
            settings = {
                self.KEY_INSTRUMENT_ID: instrument[self.KEY_ID],
                self.KEY_MEASUREMENT: "Get DC current",
                self.KEY_GAIN: 2.0,
                self.KEY_OFFSET: 1.0
            }
            self.update_measurement(name, name, settings)


if __name__ == "__main__":

    import pylint
    from tests.unit_tests.test_test_configuration import TestTestConfiguration

    TestTestConfiguration().run(True)
    pylint.run_pylint([__file__])
