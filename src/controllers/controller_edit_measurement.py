"""
Controller for editing a measurement.
"""

import wx

from src.models.id_manager import IdManager
from src.models.instruments import get_instrument_by_name
from src.views.view_dialogs import show_confirm
from src.views.view_dialogs import show_message
from src.views.view_edit_measurement import ViewEditMeasurement


class ControllerEditMeasurement(object):

    _dlg = None
    _config = None

    ###########
    # Private #
    ###########

    @classmethod
    def _update_measurements(cls):
        cls._dlg.get_instrument()
        instrument_data = cls._config.get_instrument(cls._dlg.get_instrument())
        if instrument_data is not None:
            instrument_name = instrument_data.get(cls._config.KEY_SETTINGS, {}).get(cls._config.KEY_INSTRUMENT_NAME)
            instrument_object = get_instrument_by_name(instrument_name)
            cls._dlg.set_list_of_measurements(sorted(list(map(lambda x: x[cls._config.KEY_NAME],
                                                              instrument_object.get_input_channels()))))

    ##################
    # Event handlers #
    ##################

    @classmethod
    def _on_instrument_select(cls, event):
        cls._update_measurements()
        event.Skip()

    ##########
    # Public #
    ##########

    @classmethod
    def get_dialog(cls):
        return cls._dlg

    @classmethod
    def edit_measurement(cls, parent, configuration, name):
        dialog_title = "Add measurement"
        instrument_name = ""
        measurement_name = ""
        gain = 1.0
        offset = 0.0
        if name != "":
            measurement_data = configuration.get_measurement(name)
            measurement_name = measurement_data[configuration.KEY_SETTINGS][configuration.KEY_MEASUREMENT]
            instrument_id = measurement_data[configuration.KEY_SETTINGS][configuration.KEY_INSTRUMENT_ID]
            instrument = configuration.get_instrument(instrument_id)
            if instrument is not None:
                instrument_name = instrument[configuration.KEY_NAME]
            gain = measurement_data[configuration.KEY_SETTINGS][configuration.KEY_GAIN]
            offset = measurement_data[configuration.KEY_SETTINGS][configuration.KEY_OFFSET]
        cls._config = configuration
        cls._dlg = ViewEditMeasurement(parent, dialog_title, configuration, name)
        cls._dlg.set_list_of_instruments(sorted(list(map(lambda x: x[configuration.KEY_NAME],
                                                     configuration.get_instruments()))))
        cls._dlg.set_name(name)
        cls._dlg.set_instrument(instrument_name)
        cls._update_measurements()
        cls._dlg.set_measurement(measurement_name)
        cls._dlg.set_gain(gain)
        cls._dlg.set_offset(offset)
        cls._dlg.Bind(wx.EVT_COMBOBOX, cls._on_instrument_select, id=IdManager.ID_CMB_MEASUREMENT_INSTRUMENT)
        if cls._dlg.ShowModal() == wx.ID_OK:
            new_name = cls._dlg.get_name()
            settings = {
                configuration.KEY_INSTRUMENT_ID: cls._dlg.get_instrument(),
                configuration.KEY_MEASUREMENT: cls._dlg.get_measurement(),
                configuration.KEY_GAIN: cls._dlg.get_gain(),
                configuration.KEY_OFFSET: cls._dlg.get_offset()
            }
            configuration.update_measurement(name, new_name, settings)
        cls._dlg.Destroy()
        cls._dlg = None
        wx.YieldIfNeeded()

    @classmethod
    def delete_measurement(cls, parent, configuration):
        dialog_title = "Delete measurement"
        name = parent.get_selected_measurement()
        if name is None:
            show_message(parent, "Select a measurement first", dialog_title)
        else:
            if show_confirm(parent, "Do you want to delete measurement '{}'?".format(name), dialog_title) == wx.ID_YES:
                configuration.delete_measurement(name)
        wx.YieldIfNeeded()


if __name__ == "__main__":

    from tests.unit_tests.test_controller_edit_measurement import TestControllerEditInstrument

    TestControllerEditInstrument().run(True)

