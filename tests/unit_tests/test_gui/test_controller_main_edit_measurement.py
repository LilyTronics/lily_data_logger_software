"""
Test edit instrument for the main controller.
"""

import wx.grid

from src.models.id_manager import IdManager
from tests.unit_tests.test_gui.test_controller_main import TestControllerMain


class TestControllerMainEditMeasurement(TestControllerMain):

    def _add_instrument(self):
        result = ""
        self.gui.click_button(IdManager.ID_BTN_ADD_INSTRUMENT)
        if not self.gui.wait_until_window_available(IdManager.ID_TEST_CONSOLE):
            result += "\nThe edit instrument dialog did not appear"
        else:
            self.log.debug("Add instrument")
            self.gui.set_value_in_control(IdManager.ID_INSTRUMENT_NAME, "Test instrument")
            self.gui.set_value_in_control(IdManager.ID_CMB_INSTRUMENT, "Simulator multimeter")
            self.gui.click_button(wx.ID_OK)
            self.log.debug("Check if instrument is in the list")
            list_control = self.gui.get_window(IdManager.ID_LIST_INSTRUMENTS)
            self.wait_for(list_control.GetItemCount, 1, 1, 0.1)
            if list_control.GetItemCount() < 1:
                result += "\nThe instrument is not in the list"
        return result

    def _add_measurement(self):
        result = self._add_instrument()
        if result == "":
            self.gui.click_button(IdManager.ID_BTN_ADD_MEASUREMENT)
            if not self.gui.wait_until_window_available(IdManager.ID_OFFSET):
                result += "\nThe edit measurement dialog did not appear"
            else:
                self.log.debug("Add measurement")
                self.gui.set_value_in_control(IdManager.ID_MEASUREMENT_NAME, "Voltage")
                self.gui.set_value_in_control(IdManager.ID_CMB_MEASUREMENT_INSTRUMENT,
                                              "Test instrument")
                combo = self.gui.get_window(IdManager.ID_CMB_MEASUREMENT)
                self.wait_for(combo.GetCount, 2, 1, 0.1)
                self.gui.set_value_in_control(IdManager.ID_CMB_MEASUREMENT, "Get DC voltage")
                self.gui.click_button(wx.ID_OK)
                self.log.debug("Check if measurement is in the grid")
                grid_control = self.gui.get_window(IdManager.ID_GRID_MEASUREMENTS)
                if not self.wait_for(grid_control.GetNumberCols, 2, 1, 0.1):
                    result += "\nMeasurement was not added to the grid"
                elif grid_control.GetColLabelValue(1) != "Voltage":
                    result += "\nMeasurement name in the grid is not correct"
        return result

    def test_add_measurement(self):
        def _test_add_measurement():
            result = self._add_measurement()
            result += self.close_view_main(True)
            return result

        self.show_view_main(_test_add_measurement)

    def test_edit_measurement(self):
        def _test_edit_measurement():
            def _get_measurement_name():
                return grid_control.GetColLabelValue(1)

            result = self._add_measurement()
            if result == "":
                self.log.debug("Edit measurement")
                grid_control = self.gui.get_window(IdManager.ID_GRID_MEASUREMENTS)
                grid_control.SelectCol(1)
                self.gui.post_event(grid_control, wx.grid.wxEVT_GRID_LABEL_LEFT_DCLICK,
                                    grid_control.GetId())
                if not self.gui.wait_until_window_available(IdManager.ID_OFFSET):
                    result += "\nThe edit measurement dialog did not appear"
                else:
                    self.log.debug("Change values")
                    self.gui.set_value_in_control(IdManager.ID_MEASUREMENT_NAME, "Voltage T1")
                    self.gui.click_button(wx.ID_OK)
                    self.log.debug("Check if measurement is in the grid")
                    grid_control = self.gui.get_window(IdManager.ID_GRID_MEASUREMENTS)
                    if not self.wait_for(_get_measurement_name, "Voltage T1", 1, 0.1):
                        result += "\nMeasurement name in the grid is not correct"
            result += self.close_view_main(True)
            return result

        self.show_view_main(_test_edit_measurement)

    def test_delete_measurement(self):
        def _test_delete_instrument():
            result = self._add_measurement()
            if result == "":
                self.log.debug("Delete measurement")
                grid_control = self.gui.get_window(IdManager.ID_GRID_MEASUREMENTS)
                grid_control.SelectCol(1)
                self.gui.click_button(IdManager.ID_BTN_DELETE_MEASUREMENT)
                if not self.gui.wait_for_dialog(self.view_main, True):
                    result += "\nThe dialog did not appear while we expected one"
                else:
                    self.gui.send_key_press(self.gui.KEY_ENTER)
                    if not self.wait_for(grid_control.GetNumberCols, 1, 1, 0.1):
                        result += "\nThe measurement was not removed from the grid"
            result += self.close_view_main(True)
            return result

        self.show_view_main(_test_delete_instrument)


if __name__ == "__main__":

    import pylint

    TestControllerMainEditMeasurement().run(True)
    pylint.run_pylint([__file__])
