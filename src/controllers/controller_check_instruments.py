"""
Controller for checking the instruments.
"""

import threading
import wx

from src.models.id_manager import IdManager
from src.models.instrument_pool import InstrumentPool
from src.views.view_check_instruments import ViewCheckInstruments


class ControllerCheckInstruments:

    def __init__(self, parent, configuration):
        self._config = configuration
        self._view = ViewCheckInstruments(parent)
        self._view.add_instruments(map(lambda x: x[self._config.KEY_NAME],
                                       self._config.get_instruments()))
        self._view.Bind(wx.EVT_BUTTON, self._on_check_click, id=IdManager.ID_BTN_CHECK)
        self._view.ShowModal()
        self._view.Destroy()

    ###########
    # Private #
    ###########

    def _check_instruments(self):
        instruments = self._config.get_instruments()
        if len(instruments) == 0:
            return
        self._view.active_dialog = wx.ProgressDialog("Checking instruments", " ", len(instruments),
                                                     self._view, wx.PD_CAN_ABORT | wx.PD_APP_MODAL |
                                                     wx.PD_AUTO_HIDE)
        i = 0
        t = None
        while i < len(instruments):
            if t is None:
                instrument_name = instruments[i][self._config.KEY_NAME]
                message = f"Checking instrument: '{instrument_name}' . . ."
                self._view.active_dialog.Update(i, message)
                t = threading.Thread(target=self._check_instrument, args=(instruments[i], ))
                t.daemon = True
                t.start()
            elif not t.is_alive():
                t = None
                i += 1
            wx.MilliSleep(100)
            do_continue, _ = self._view.active_dialog.Update(i)
            if not do_continue:
                break
        self._view.active_dialog.Destroy()
        self._view.active_dialog = None
        wx.YieldIfNeeded()

    def _check_instrument(self, instrument_data):
        instrument_name = instrument_data[self._config.KEY_NAME]
        self._update_status(instrument_name, None, "")
        InstrumentPool.clear_instruments()
        result = "Connection OK"
        try:
            instrument = InstrumentPool.create_instrument(instrument_data)
            instrument.initialize()
            instrument.start()
            input_channels = instrument.get_input_channels()
            if len(input_channels) > 0:
                channel_name = input_channels[0][instrument.KEY_NAME]
                value = instrument.process_channel(channel_name)
                if isinstance(value, str) and value.startswith("ERROR: "):
                    raise Exception(value)
                result += f" ({channel_name} = {value})"
            self._update_status(instrument_name, True, result)
        except Exception as e:
            self._update_status(instrument_name, False, str(e))
        InstrumentPool.clear_instruments()

    def _update_status(self, instrument_id, is_passed, message):
        wx.CallAfter(self._view.update_instrument, instrument_id, is_passed, message)

    ##################
    # Event handlers #
    ##################

    def _on_check_click(self, event):
        wx.CallAfter(self._check_instruments)
        event.Skip()


if __name__ == "__main__":

    from tests.unit_tests.test_gui.test_controller_check_instruments import (
        TestControllerCheckInstrument)

    TestControllerCheckInstrument().run(True)
