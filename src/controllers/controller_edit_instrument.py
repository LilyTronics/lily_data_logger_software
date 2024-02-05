"""
Controller for editing instruments.
"""

import wx

from src.models.id_manager import IdManager
from src.models.instruments import get_instrument_names
from src.models.instruments import get_instrument_by_name
from src.models.interfaces import get_interface_by_name
from src.views.view_edit_instrument import ViewEditInstrument


class ControllerEditInstrument(object):

    _dlg = None

    ##################
    # Event handlers #
    ##################

    @classmethod
    def _on_instrument_select(cls, event):
        cls._dlg.set_instrument_info("")
        cls._dlg.update_instrument_settings_controls({})
        instrument_name = cls._dlg.get_selected_instrument_name()
        if instrument_name != "":
            instrument = get_instrument_by_name(instrument_name)
            cls._dlg.set_instrument_info(instrument.get_info())
            interface_type = instrument.get_interface_type()
            if interface_type is not None:
                interface = get_interface_by_name(interface_type)
                settings_controls = interface.get_settings_controls()
                instrument_defaults = instrument.get_interface_settings()
                for key in instrument_defaults.keys():
                    settings_controls[key]["default"] = str(instrument_defaults[key])
                cls._dlg.update_instrument_settings_controls(settings_controls)
        event.Skip()

    @classmethod
    def add_instrument(cls, parent):
        cls._dlg = ViewEditInstrument(parent, "Add instrument")
        cls._dlg.set_instrument_names(get_instrument_names())
        cls._dlg.Bind(wx.EVT_COMBOBOX, cls._on_instrument_select, id=IdManager.ID_CMB_INSTRUMENT)
        cls._dlg.ShowModal()
        cls._dlg.Destroy()
        cls._dlg = None


if __name__ == "__main__":

    app = wx.App(redirect=False)

    ControllerEditInstrument.add_instrument(None)
