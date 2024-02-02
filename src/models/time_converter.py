"""
Module with time converter functions.
"""

TIME_UNITS = {"seconds": 1, "minutes": 60, "hours": 3600, "days": 86400}


def create_duration_time_string(seconds):
    d, h = divmod(seconds, 86400)
    m, s = divmod(h, 60)
    h, m = divmod(m, 60)
    output = ""
    if d > 0:
        output = "{} days, ".format(d)
    output += "{:02}:{:02}:{:02}".format(h, m, s)
    return output


def convert_seconds_to_time_with_unit(seconds):
    factor = 1
    for factor in sorted(TIME_UNITS.values(), reverse=True):
        if seconds % factor == 0:
            break
    unit = list(TIME_UNITS.keys())[list(TIME_UNITS.values()).index(factor)]
    return int(seconds / factor), unit


if __name__ == "__main__":

    from tests.unit_tests.test_time_converter import TestTimeConverter

    TestTimeConverter().run()
