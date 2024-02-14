"""
Module with time converter functions.
"""


class TimeConverter(object):

    TIME_UNIT_TO_FACTOR = {"seconds": 1, "minutes": 60, "hours": 3600, "days": 86400}
    TIME_UNITS = list(TIME_UNIT_TO_FACTOR.keys())

    @staticmethod
    def create_duration_time_string(seconds):
        d, h = divmod(seconds, 86400)
        m, s = divmod(h, 60)
        h, m = divmod(m, 60)
        output = ""
        if d > 0:
            output = "{} days, ".format(d)
        output += "{:02}:{:02}:{:02}".format(h, m, s)
        return output

    @classmethod
    def convert_seconds_to_time_with_unit(cls, seconds):
        factor = 1
        for factor in sorted(cls.TIME_UNIT_TO_FACTOR.values(), reverse=True):
            if seconds % factor == 0:
                break
        unit = list(cls.TIME_UNIT_TO_FACTOR.keys())[list(cls.TIME_UNIT_TO_FACTOR.values()).index(factor)]
        return int(seconds / factor), unit

    @classmethod
    def convert_time_with_unit_to_seconds(cls, value, unit):
        if value > 0:
            matches = list(filter(lambda x: x == unit, cls.TIME_UNIT_TO_FACTOR.keys()))
            if len(matches) == 1:
                value *= cls.TIME_UNIT_TO_FACTOR[matches[0]]
        return value


if __name__ == "__main__":

    from tests.unit_tests.test_time_converter import TestTimeConverter

    TestTimeConverter().run(True)
