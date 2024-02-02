"""
Test time converter functions.
"""

from src.models.time_converter import convert_seconds_to_time_with_unit
from src.models.time_converter import create_duration_time_string
from tests.test_suite import TestSuite


class TestTimeConverter(TestSuite):

    def test_create_duration_time_string(self):
        test_values = [
            (10, "00:00:10"),
            (200, "00:03:20"),
            (4000, "01:06:40"),
            (200000, "2 days, 07:33:20"),
        ]
        for test_value in test_values:
            self.fail_if(create_duration_time_string(test_value[0]) != test_value[1],
                         "Time string is incorrect")

    def test_convert_seconds_to_time_with_unit(self):
        test_values = [
            (10, (10, "seconds")),
            (7200, (2, "hours")),
            (180, (3, "minutes")),
            (345600, (4, "days")),
        ]
        for test_value in test_values:
            self.fail_if(convert_seconds_to_time_with_unit(test_value[0]) != test_value[1],
                         "Time string is incorrect")


if __name__ == "__main__":

    TestTimeConverter().run()
