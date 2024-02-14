"""
Module with time converter functions.
"""


class TimeConverter(object):

    TIME_UNITS = {"seconds": 1, "minutes": 60, "hours": 3600, "days": 86400}

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
        for factor in sorted(cls.TIME_UNITS.values(), reverse=True):
            if seconds % factor == 0:
                break
        unit = list(cls.TIME_UNITS.keys())[list(cls.TIME_UNITS.values()).index(factor)]
        return int(seconds / factor), unit


if __name__ == "__main__":

    from tests.unit_tests.test_time_converter import TestTimeConverter

    TestTimeConverter().run()
