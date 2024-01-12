"""
This file is automatically generated by the instruments/_generate_instrument_data.py script.
"""

import base64


class InstrumentData(object):

    simulator_multimeter = base64.b64decode(
        b'eyJuYW1lIjogIlNpbXVsYXRvciBtdWx0aW1ldGVyIn0='
    )

    simulator_temperature_chamber = base64.b64decode(
        b'eyJuYW1lIjogIlNpbXVsYXRvciB0ZW1wZXJhdHVyZSBjaGFtYmVyIn0='
    )


if __name__ == '__main__':

    import json

    print(json.loads(InstrumentData.simulator_multimeter))
    print(json.loads(InstrumentData.simulator_temperature_chamber))
