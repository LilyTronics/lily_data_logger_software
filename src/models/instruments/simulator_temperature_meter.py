"""
Model for the temperature meter simulator
"""

from src.models.instrument import Instrument
from src.simulators.simulator_settings import SimulatorSettings


simulator_temperature_meter = Instrument({
    "name": "Simulator temperature meter",
    "info": "Read random values for temperature (18...22)",
    "interface": {
        "type": "Ethernet TCP",
        "settings": {
            "ip_address": SimulatorSettings.TemperatureMeterTcp.IP,
            "ip_port": SimulatorSettings.TemperatureMeterTcp.PORT,
            "rx_timeout": SimulatorSettings.TemperatureMeterTcp.RX_TIME_OUT
        }
    },
    "initialize": [
        {
            "command": "instrument_delay:0.5"
        }
    ],
    "channels": [
        {
            "name": "Get temperature",
            "type": "input",
            "command_list": [
                {
                    "command": "T?\n",
                    "response": "T={float}C\n"
                }
            ]
        }
    ]
})


if __name__ == "__main__":

    from tests.unit_tests.test_models.test_simulator_temperature_meter import (
        TestSimulatorTemperatureMeter)

    TestSimulatorTemperatureMeter().run(True)
