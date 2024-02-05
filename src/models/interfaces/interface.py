"""
Base class for all the interfaces.
"""


class Interface(object):

    def __del__(self):
        try:
            self.close()
        except (Exception, ):
            pass

    def raise_connection_exception(self, params):
        raise Exception(f"Could not connect to {params}")

    def raise_timeout_exception(self):
        raise Exception("Error receiver timeout")

    def send_command(self, command, expect_response):
        raise NotImplementedError("This method must be implemented in the derived class")

    def close(self):
        raise NotImplementedError("This method must be implemented in the derived class")

    @classmethod
    def get_settings_controls(cls):
        raise NotImplementedError("This method must be implemented in the derived class")
