"""
Test time converter functions.
"""

from src.models.time_converter import TimeConverter
from tests.unit_tests.lib.test_suite import TestSuite


class TestTimeConverter(TestSuite):

    def test_create_duration_time_string(self):
        test_values = [
            (10, "00:00:10"),
            (200, "00:03:20"),
            (4000, "01:06:40"),
            (200000, "2 days, 07:33:20"),
        ]
        for test_value in test_values:
            self.fail_if(TimeConverter.create_duration_time_string(test_value[0]) != test_value[1],
                         "Time string is incorrect")

    def test_convert_seconds_to_time_with_unit(self):
        test_values = [
            (10, (10, "seconds")),
            (7200, (2, "hours")),
            (180, (3, "minutes")),
            (345600, (4, "days")),
        ]
        for test_value in test_values:
            self.fail_if(TimeConverter.convert_seconds_to_time_with_unit(test_value[0]) !=
                         test_value[1], "Time value is incorrect")

    def test_convert_time_with_unit_to_seconds(self):
        test_values = [
            ((0, ""), 0),
            ((1, ""), 1),
            ((5, "seconds"), 5),
            ((4, "minutes"), 240),
            ((3, "hours"), 10800),
            ((2, "days"), 172800),
        ]
        for test_value in test_values:
            self.fail_if(TimeConverter.convert_time_with_unit_to_seconds(*test_value[0]) !=
                         test_value[1], "Time value is incorrect")

    def test_create_time_stamp(self):
        test_value = (1708959067, "20240226 15:51:07")
        self.fail_if(TimeConverter.get_timestamp(test_value[0]) != test_value[1],
                     "Timestamp is not correct")


if __name__ == "__main__":

    import pylint

    TestTimeConverter().run(True)
    pylint.run_pylint([__file__])
