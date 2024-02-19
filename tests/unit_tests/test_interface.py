"""
Test the interface base class.
"""

from src.models.interfaces.interface import Interface
from tests.unit_tests.lib.test_suite import TestSuite


class TestInterface(TestSuite):

    class _TestInterface(Interface):

        def __init__(self, param1, param2, param3):
            params_to_match = {
                "param1": param1,
                "param2": param2,
            }
            super().__init__(params_to_match)
            self._params = (param1, param2, param3)

        def close(self):
            pass

        @classmethod
        def get_settings_controls(cls):
            pass

        def send_command(self, command, expect_response, pre_response, post_response):
            pass

    def test_is_match(self):
        test_interface = self._TestInterface("value1", "value2", "value3")
        self.log.debug("Match with the same parameters and values should be a match")
        match = test_interface.is_match({"param1": "value1", "param2": "value2"})
        self.log.debug(f"Is match: {match}")
        self.fail_if(not match, "The interface did not match with the same parameters")
        self.log.debug("Match with a different value should not be a match")
        match = test_interface.is_match({"param1": "value1", "param2": "value3"})
        self.log.debug(f"Is match: {match}")
        self.fail_if(match, "The interface did match with a different value")
        self.log.debug("Match with a missing parameter should not be a match")
        match = test_interface.is_match({"param1": "value1", "param3": "value3"})
        self.log.debug(f"Is match: {match}")
        self.fail_if(match, "The interface did match with a missing parameter")


if __name__ == "__main__":

    import pylint

    TestInterface().run(True)
    pylint.run_pylint([__file__])
