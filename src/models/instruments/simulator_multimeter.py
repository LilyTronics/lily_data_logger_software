"""
Model for the multimeter simulator
"""

from src.models.instrument import Instrument
from src.simulators.simulator_settings import SimulatorSettings


simulator_multimeter = Instrument({
    "name": "Simulator multimeter",
    "info": "Read random values for voltage (4.9...5.1V) and current (0.39...0.41)",
    "interface": {
        "type": "Ethernet UDP",
        "settings": {
            "ip_address": SimulatorSettings.MultimeterUdp.IP,
            "ip_port": SimulatorSettings.MultimeterUdp.PORT,
            "rx_timeout": SimulatorSettings.MultimeterUdp.RX_TIME_OUT
        }
    },
    "channels": [
        {
            "name": "Get DC voltage",
            "type": "input",
            "command_list": [
                {
                    "command": "VDC?\n",
                    "response": "VDC={float}V\n"
                }
            ]
        },
        {
            "name": "Get DC current",
            "type": "input",
            "command_list": [
                {
                    "command": "ADC?\n",
                    "response": "ADC={float}A\n"
                }
            ]
        },
    ]
})


if __name__ == "__main__":

    from tests.unit_tests.test_simulator_multimeter import TestSimulatorMultimeter

    TestSimulatorMultimeter().run()
