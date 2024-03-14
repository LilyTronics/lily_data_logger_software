"""
Manages ID for various purposes
"""

import wx


class IdManager:

    # View main
    ID_TOOL_NEW_CONFIGURATION = 100
    ID_TOOL_OPEN_CONFIGURATION = 101
    ID_TOOL_SAVE_CONFIGURATION = 102
    ID_TOOL_EDIT_CONFIGURATION = 103
    ID_TOOL_CHECK_INSTRUMENTS = 104
    ID_TOOL_START_PROCESS = 105
    ID_TOOL_STOP_PROCESS = 106
    ID_TOOL_EXPORT_CSV = 107
    ID_TOOL_EXPORT_INSTRUMENT = 108
    ID_TOOL_SHOW_LOG = 109

    ID_RECENT_CONFIG_MENU = 110

    ID_TOOL_TEST_CONFIG = 199

    ID_LABEL_SAMPLE_TIME = 200
    ID_LABEL_END_TIME = 201
    ID_LABEL_TOTAL_SAMPLES = 202
    ID_LABEL_ELAPSED_TIME = 203

    ID_LIST_INSTRUMENTS = 300
    ID_BTN_ADD_INSTRUMENT = 301
    ID_BTN_DELETE_INSTRUMENT = 302

    ID_GRID_MEASUREMENTS = 400
    ID_BTN_ADD_MEASUREMENT = 401
    ID_BTN_DELETE_MEASUREMENT = 402

    # View edit configuration
    ID_SAMPLE_TIME = 500
    ID_SAMPLE_TIME_UNITS = 501
    ID_END_TIME = 502
    ID_END_TIME_UNITS = 503
    ID_FIXED = 504
    ID_CONTINUOUS = 505
    ID_TOTAL_SAMPLES = 506

    # View edit instrument
    ID_INSTRUMENT_NAME = 600
    ID_CMB_INSTRUMENT = 601
    ID_TEST_CONSOLE = 602
    ID_BTN_SETTINGS_TEST = 603

    # View check instruments
    ID_BTN_CHECK = 700

    # View edit measurement
    ID_MEASUREMENT_NAME = 800
    ID_CMB_MEASUREMENT_INSTRUMENT = 801
    ID_CMB_MEASUREMENT = 802
    ID_GAIN = 803
    ID_OFFSET = 804

    # View log
    ID_LOG_MESSAGES = 900

    _RESERVED_WIDGET_IDS = sorted(list(map(lambda y: getattr(wx, y),
                                           filter(lambda x: x.startswith("ID_"), dir(wx)))))
    _WIDGET_START_ID = 100
    _WIDGET_END_ID = 32000

    def __init__(self):
        # Prevent creating instances
        raise RuntimeError("No instance of this class is permitted")

    @classmethod
    def get_reserved_widgets_ids(cls):
        return cls._RESERVED_WIDGET_IDS


if __name__ == "__main__":

    from tests.unit_tests.test_models.test_id_manager import TestIdManager

    TestIdManager().run(True)
