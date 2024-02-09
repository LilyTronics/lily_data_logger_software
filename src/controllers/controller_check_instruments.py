"""
Controller for checking the instruments.
"""

import threading
import wx

from src.models.id_manager import IdManager
from src.models.instruments import get_instrument_by_name
from src.models.interfaces import get_interface_by_name
from src.views.view_check_instruments import ViewCheckInstruments


class ControllerCheckInstruments(object):

    def __init__(self, parent, configuration):
        self._config = configuration
        self._view = ViewCheckInstruments(parent)
        self._view.add_instruments(map(lambda x: x[self._config.KEY_NAME], self._config.get_instruments()))
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
                                                     self._view, wx.PD_CAN_ABORT | wx.PD_APP_MODAL)
        i = 0
        t = None
        while i < len(instruments):
            instrument_name = instruments[i][self._config.KEY_NAME]
            do_continue, can_skip = self._view.active_dialog.Update(i, "Checking instrument: '{}' . . .".format(
                instrument_name))
            if not do_continue:
                break
            wx.MilliSleep(100)
            if t is None:
                t = threading.Thread(target=self._check_instrument, args=(instrument_name, ))
                t.daemon = True
                t.start()
            else:
                if not t.is_alive():
                    t = None
                    i += 1
        self._view.active_dialog.Destroy()
        self._view.active_dialog = None
        wx.YieldIfNeeded()

    def _check_instrument(self, instrument_name):
        self._update_status(instrument_name, None, "")
        interface_object = None
        try:
            instrument_data = self._config.get_instrument(instrument_name)
            assert instrument_data is not None, "Instrument '{}' not in the configuration".format(instrument_name)
            settings = instrument_data.get(self._config.KEY_SETTINGS, None)
            assert settings is not None, "Instrument '{}' has no settings".format(instrument_name)
            instrument_definition = settings.get(self._config.KEY_INSTRUMENT, None)
            assert instrument_definition is not None, "Instrument '{}' has no instrument defined".format(
                instrument_definition)
            instrument_object = get_instrument_by_name(instrument_definition)
            assert instrument_object is not None, "Instrument definition '{}' does not exist".format(
                instrument_definition)
            interface_type = instrument_object.get_interface_type()
            assert interface_type is not None, "No interface defined in instrument definition '{}'".format(
                instrument_definition)
            interface_class = get_interface_by_name(interface_type)
            assert interface_class is not None, "Interface type '{}' does not exist".format(interface_type)
            instrument_defaults = instrument_object.get_interface_settings()
            instrument_settings = settings.get(self._config.KEY_INSTRUMENT_SETTINGS, {})
            for key in instrument_defaults.keys():
                if key not in instrument_settings.keys():
                    instrument_settings[key] = instrument_defaults[key]
            interface_object = interface_class(**instrument_settings)
            instrument_object.set_interface_object(interface_object)
            instrument_object.initialize()
            result = "Connection OK"
            input_channels = instrument_object.get_input_channels()
            if len(input_channels) > 0:
                channel_name = input_channels[0][instrument_object.KEY_NAME]
                value = instrument_object.get_value(channel_name)
                result += " ({} = {})".format(channel_name, value)
            self._update_status(instrument_name, True, result)
        except Exception as e:
            self._update_status(instrument_name, False, str(e))
        finally:
            if interface_object is not None:
                interface_object.close()

    def _update_status(self, instrument_id, is_passed, message):
        wx.CallAfter(self._view.update_instrument, instrument_id, is_passed, message)

    ##################
    # Event handlers #
    ##################

    def _on_check_click(self, event):
        wx.CallAfter(self._check_instruments)
        event.Skip()


if __name__ == "__main__":

    from tests.unit_tests.test_controller_check_instruments import TestControllerCheckInstrument

    TestControllerCheckInstrument().run()
