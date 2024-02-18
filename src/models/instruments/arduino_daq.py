"""
Model for the Arduino Uno DAQ.
"""

from src.models.instrument import Instrument


arduino_daq = Instrument({
    "name": "Arduino DAQ",
    "info": "Read and write digital IO and read analog values with an Arduino",
    "interface": {
        "type": "Serial port",
        "settings": {
            "baud_rate": 115200
        }
    },
    "initialize": [
        {
            "command": "interface:toggle_dtr"
        },
        {
            "command": "instrument_delay:2"
        },
        {
            "command": "rd2\n",
            "response": "{int}\n"
        },
    ],
    "channels": [
        ###################
        # Read digital IO #
        ###################
        {
            "name": "D2 get state",
            "type": "input",
            "command_list": [
                {
                    "command": "rd2\n",
                    "response": "{int}\n"
                }
            ]
        },
        {
            "name": "D3 get state",
            "type": "input",
            "command_list": [
                {
                    "command": "rd3\n",
                    "response": "{int}\n"
                }
            ]
        },
        {
            "name": "D4 get state",
            "type": "input",
            "command_list": [
                {
                    "command": "rd4\n",
                    "response": "{int}\n"
                }
            ]
        },
        {
            "name": "D5 get state",
            "type": "input",
            "command_list": [
                {
                    "command": "rd5\n",
                    "response": "{int}\n"
                }
            ]
        },
        {
            "name": "D6 get state",
            "type": "input",
            "command_list": [
                {
                    "command": "rd6\n",
                    "response": "{int}\n"
                }
            ]
        },
        {
            "name": "D7 get state",
            "type": "input",
            "command_list": [
                {
                    "command": "rd7\n",
                    "response": "{int}\n"
                }
            ]
        },
        {
            "name": "D8 get state",
            "type": "input",
            "command_list": [
                {
                    "command": "rd8\n",
                    "response": "{int}\n"
                }
            ]
        },
        {
            "name": "D9 get state",
            "type": "input",
            "command_list": [
                {
                    "command": "rd9\n",
                    "response": "{int}\n"
                }
            ]
        },
        {
            "name": "D10 get state",
            "type": "input",
            "command_list": [
                {
                    "command": "rd10\n",
                    "response": "{int}\n"
                }
            ]
        },
        {
            "name": "D11 get state",
            "type": "input",
            "command_list": [
                {
                    "command": "rd11\n",
                    "response": "{int}\n"
                }
            ]
        },
        {
            "name": "D12 get state",
            "type": "input",
            "command_list": [
                {
                    "command": "rd12\n",
                    "response": "{int}\n"
                }
            ]
        },
        {
            "name": "D13 get state",
            "type": "input",
            "command_list": [
                {
                    "command": "rd13\n",
                    "response": "{int}\n"
                }
            ]
        },
        #################
        # Write digital #
        #################
        {
            "name": "D2 set state",
            "type": "output",
            "command_list": [
                {
                    "command": "wd2 {int}\n"
                }
            ]
        },
        {
            "name": "D3 set state",
            "type": "output",
            "command_list": [
                {
                    "command": "wd3 {int}\n"
                }
            ]
        },
        {
            "name": "D4 set state",
            "type": "output",
            "command_list": [
                {
                    "command": "wd4 {int}\n"
                }
            ]
        },
        {
            "name": "D5 set state",
            "type": "output",
            "command_list": [
                {
                    "command": "wd5 {int}\n"
                }
            ]
        },
        {
            "name": "D6 set state",
            "type": "output",
            "command_list": [
                {
                    "command": "wd6 {int}\n"
                }
            ]
        },
        {
            "name": "D7 set state",
            "type": "output",
            "command_list": [
                {
                    "command": "wd7 {int}\n"
                }
            ]
        },
        {
            "name": "D8 set state",
            "type": "output",
            "command_list": [
                {
                    "command": "wd8 {int}\n"
                }
            ]
        },
        {
            "name": "D9 set state",
            "type": "output",
            "command_list": [
                {
                    "command": "wd9 {int}\n"
                }
            ]
        },
        {
            "name": "D10 set state",
            "type": "output",
            "command_list": [
                {
                    "command": "wd10 {int}\n"
                }
            ]
        },
        {
            "name": "D11 set state",
            "type": "output",
            "command_list": [
                {
                    "command": "wd11 {int}\n"
                }
            ]
        },
        {
            "name": "D12 set state",
            "type": "output",
            "command_list": [
                {
                    "command": "wd12 {int}\n"
                }
            ]
        },
        {
            "name": "D13 set state",
            "type": "output",
            "command_list": [
                {
                    "command": "wd13 {int}\n"
                }
            ]
        },
        ######################
        # Read analog inputs #
        ######################
        {
            "name": "A0 get voltage",
            "type": "input",
            "command_list": [
                {
                    "command": "ra0\n",
                    "response": "{float}\n"
                }
            ]
        },
        {
            "name": "A1 get voltage",
            "type": "input",
            "command_list": [
                {
                    "command": "ra1\n",
                    "response": "{float}\n"
                }
            ]
        },
        {
            "name": "A2 get voltage",
            "type": "input",
            "command_list": [
                {
                    "command": "ra2\n",
                    "response": "{float}\n"
                }
            ]
        },
        {
            "name": "A3 get voltage",
            "type": "input",
            "command_list": [
                {
                    "command": "ra3\n",
                    "response": "{float}\n"
                }
            ]
        },
        {
            "name": "A4 get voltage",
            "type": "input",
            "command_list": [
                {
                    "command": "ra4\n",
                    "response": "{float}\n"
                }
            ]
        },
        {
            "name": "A5 get voltage",
            "type": "input",
            "command_list": [
                {
                    "command": "ra5\n",
                    "response": "{float}\n"
                }
            ]
        }
    ]
})


if __name__ == "__main__":

    import pylint
    from tests.unit_tests.test_arduino_daq import TestArduinoDAQ

    TestArduinoDAQ().run(True)
    pylint.run_pylint([__file__])
