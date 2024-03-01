"""
Test for the controller edit measurement.
"""

import wx

from src.controllers.controller_edit_measurement import ControllerEditMeasurement
from src.models.configuration import Configuration
from src.models.id_manager import IdManager
from tests.unit_tests.lib.test_suite import TestSuite


class TestControllerEditInstrument(TestSuite):

    _thread_timeout = 10
    _app = None
    _error = ""

    @staticmethod
    def _create_config(add_measurement=False):
        conf = Configuration()
        name = "Test instrument"
        settings = {
            conf.KEY_INSTRUMENT_NAME: "Simulator multimeter",
            conf.KEY_INSTRUMENT_SETTINGS: {
                "ip_address": "localhost",
                "ip_port": 17000,
                "rx_timeout": 0.2
            }
        }
        conf.update_instrument(name, name, settings)
        if add_measurement:
            instrument = conf.get_instrument(name)
            name = "Current"
            settings = {
                conf.KEY_INSTRUMENT_ID: instrument[conf.KEY_ID],
                conf.KEY_MEASUREMENT: "Get DC current",
                conf.KEY_GAIN: 2.0,
                conf.KEY_OFFSET: 1.0
            }
            conf.update_measurement(name, name, settings)
        return conf

    def setup(self):
        self._app = self.gui.get_wx_app()

    # pylint: disable=too-many-statements
    def test_add_measurement(self):
        def _check_for_dialog():
            if not self.gui.wait_for_dialog(ControllerEditMeasurement.get_dialog(), True):
                self._error = "expected dialog did not appear"
                self.gui.click_button(wx.ID_CANCEL)
            if self._error == "":
                self.gui.send_key_press(self.gui.KEY_ENTER)
            if not self.gui.wait_for_dialog(ControllerEditMeasurement.get_dialog(), False):
                self._error = "dialog did not close"

        def _test_add_measurement():
            if not self.gui.wait_until_window_available(IdManager.ID_OFFSET):
                self._error = "the edit measurement dialog did not appear"
            else:
                self.log.debug("Test no name")
                self.gui.set_value_in_control(IdManager.ID_MEASUREMENT_NAME, "")
                self.gui.click_button(wx.ID_OK)
                _check_for_dialog()
                if self._error == "":
                    self.log.debug("Test no instrument")
                    self.gui.set_value_in_control(IdManager.ID_MEASUREMENT_NAME, "Current")
                    self.gui.set_value_in_control(IdManager.ID_CMB_MEASUREMENT_INSTRUMENT, "")
                    self.gui.click_button(wx.ID_OK)
                    _check_for_dialog()
                if self._error == "":
                    self.log.debug("Test no measurement")
                    self.gui.set_value_in_control(IdManager.ID_CMB_MEASUREMENT_INSTRUMENT,
                                                  "Test instrument")
                    self.gui.set_value_in_control(IdManager.ID_CMB_MEASUREMENT, "")
                    self.gui.click_button(wx.ID_OK)
                    _check_for_dialog()
                if self._error == "":
                    self.log.debug("Test no gain")
                    self.gui.set_value_in_control(IdManager.ID_CMB_MEASUREMENT, "Get DC current")
                    self.gui.set_value_in_control(IdManager.ID_GAIN, "")
                    self.gui.click_button(wx.ID_OK)
                    _check_for_dialog()
                if self._error == "":
                    self.log.debug("Test no offset")
                    self.gui.set_value_in_control(IdManager.ID_GAIN, "2.0")
                    self.gui.set_value_in_control(IdManager.ID_OFFSET, "")
                    self.gui.click_button(wx.ID_OK)
                    _check_for_dialog()
                if self._error == "":
                    self.log.debug("Add measurement")
                    self.gui.set_value_in_control(IdManager.ID_OFFSET, "1.0")
                    self.gui.click_button(wx.ID_OK)

        conf = self._create_config()
        self._error = ""
        t = self.start_thread(_test_add_measurement)
        ControllerEditMeasurement.edit_measurement(None, conf, "")
        self.wait_for(t.is_alive, False, self._thread_timeout, 0.1)
        self.fail_if(self._error != "", self._error)
        self.fail_if(len(conf.get_measurements()) == 0, "Measurement was not added")
        measurement = conf.get_measurement("Current")
        self.fail_if(measurement is None, "Measurement was not added")

    def test_add_same_name(self):
        def _test_add_same_name():
            if not self.gui.wait_until_window_available(IdManager.ID_OFFSET):
                self._error = "the edit measurement dialog did not appear"
            else:
                self.log.debug("Add measurement with same name")
                # Use different case, should be case-insensitive
                self.gui.set_value_in_control(IdManager.ID_MEASUREMENT_NAME, "cUrrEnT")
                self.gui.set_value_in_control(IdManager.ID_CMB_MEASUREMENT_INSTRUMENT,
                                              "Test instrument")
                self.gui.set_value_in_control(IdManager.ID_CMB_MEASUREMENT, "Get DC current")
                self.gui.click_button(wx.ID_OK)
                if not self.gui.wait_for_dialog(ControllerEditMeasurement.get_dialog(), True):
                    self._error = "expected dialog did not appear"
                if self._error == "":
                    self.gui.send_key_press(self.gui.KEY_ENTER)
                    if not self.gui.wait_for_dialog(ControllerEditMeasurement.get_dialog(), False):
                        self._error = "dialog did not close"
                self.gui.click_button(wx.ID_CANCEL)

        conf = self._create_config(True)
        self._error = ""
        t = self.start_thread(_test_add_same_name)
        ControllerEditMeasurement.edit_measurement(None, conf, "")
        self.wait_for(t.is_alive, False, self._thread_timeout, 0.1)
        self.fail_if(self._error != "", self._error)

    def test_edit_measurement(self):
        def _test_edit_measurement():
            if not self.gui.wait_until_window_available(IdManager.ID_OFFSET):
                self._error = "the edit measurement dialog did not appear"
            else:
                self.log.debug("Edit measurement")
                if self.gui.get_value_from_window(IdManager.ID_MEASUREMENT_NAME) != "Current":
                    self._error = "the measurement name is not correct"
                if (self.gui.get_value_from_window(IdManager.ID_CMB_MEASUREMENT_INSTRUMENT) !=
                        "Test instrument"):
                    self._error += "\nthe instrument name is not correct"
                if self.gui.get_value_from_window(IdManager.ID_CMB_MEASUREMENT) != "Get DC current":
                    self._error += "\nthe measurement is not correct"
                if self.gui.get_value_from_window(IdManager.ID_GAIN) != "2.0":
                    self._error += "\nthe gain is not correct"
                if self.gui.get_value_from_window(IdManager.ID_OFFSET) != "1.0":
                    self._error += "\nthe offset is not correct"
                if self._error == "":
                    self.log.debug("Change values")
                    self.gui.set_value_in_control(IdManager.ID_MEASUREMENT_NAME, "Voltage")
                    self.gui.set_value_in_control(IdManager.ID_CMB_MEASUREMENT, "Get DC voltage")
                    self.gui.set_value_in_control(IdManager.ID_GAIN, "4.0")
                    self.gui.set_value_in_control(IdManager.ID_OFFSET, "2.0")
                    self.gui.click_button(wx.ID_OK)
                else:
                    self.gui.click_button(wx.ID_CANCEL)

        conf = self._create_config(True)
        measurement = conf.get_measurements()[0]
        self._error = ""
        t = self.start_thread(_test_edit_measurement)
        ControllerEditMeasurement.edit_measurement(None, conf, measurement[conf.KEY_NAME])
        self.wait_for(t.is_alive, False, self._thread_timeout, 0.1)
        self.fail_if(self._error != "", self._error.strip())
        self.fail_if(len(conf.get_measurements()) != 1, "measurement edit failed")
        measurement = conf.get_measurement("Current")
        self.fail_if(measurement is not None, "measurement with old name was found")
        measurement = conf.get_measurement("Voltage")
        self.fail_if(measurement is None, "measurement with new name not found")
        self.fail_if(measurement[conf.KEY_SETTINGS][conf.KEY_MEASUREMENT] != "Get DC voltage",
                     "the measurement is not correct")
        self.fail_if(measurement[conf.KEY_SETTINGS][conf.KEY_GAIN] != 4.0,
                     "the gain is not correct")
        self.fail_if(measurement[conf.KEY_SETTINGS][conf.KEY_OFFSET] != 2.0,
                     "the offset is not correct")

    def teardown(self):
        self._app.Destroy()
        del self._app


if __name__ == "__main__":

    import pylint

    TestControllerEditInstrument().run(True)
    pylint.run_pylint([__file__])
