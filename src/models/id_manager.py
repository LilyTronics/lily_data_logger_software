"""
Manages ID for various purposes
"""

import wx


class IdManager(object):

    # View main
    ID_TOOL_OPEN_CONFIGURATION = 100
    ID_TOOL_SAVE_CONFIGURATION = 101
    ID_TOOL_EDIT_CONFIGURATION = 102
    ID_TOOL_CHECK_INSTRUMENTS = 103
    ID_TOOL_START_PROCESS = 104
    ID_TOOL_STOP_PROCESS = 105
    ID_TOOL_EXPORT_CSV = 106
    ID_TOOL_EXPORT_INSTRUMENT = 107
    ID_TOOL_SHOW_LOG = 108

    ID_LABEL_SAMPLE_TIME = 200
    ID_LABEL_END_TIME = 201
    ID_LABEL_TOTAL_SAMPLES = 202
    ID_LABEL_ELAPSED_TIME = 203

    ID_LIST_INSTRUMENTS = 300
    ID_BTN_ADD_INSTRUMENT = 301
    ID_BTN_DELETE_INSTRUMENT = 302

    # View edit configuration
    ID_SAMPLE_TIME = 400
    ID_SAMPLE_TIME_UNITS = 401
    ID_END_TIME = 402
    ID_END_TIME_UNITS = 403
    ID_FIXED = 404
    ID_CONTINUOUS = 405
    ID_TOTAL_SAMPLES = 406

    # View edit instrument
    ID_CMB_INSTRUMENT = 500
    ID_BTN_TEST = 501

    _RESERVED_WIDGET_IDS = sorted(list(map(lambda y: getattr(wx, y), filter(lambda x: x.startswith("ID_"), dir(wx)))))
    _WIDGET_START_ID = 100
    _WIDGET_END_ID = 32000

    def __init__(self):
        # Prevent creating instances
        raise RuntimeError("No instance of this class is permitted")

    @classmethod
    def get_reserved_widgets_ids(cls):
        return cls._RESERVED_WIDGET_IDS


if __name__ == "__main__":

    from tests.unit_tests.test_id_manager import TestIdManager

    TestIdManager().run()
