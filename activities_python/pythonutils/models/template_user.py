"""Module for the adapter user classes."""

from activities_python.pythonutils.utils import check_input_params


class TemplateUser(object):
    """Class representing the adapter user. """

    USERNAME = "username"
    PASSWORD = "password"

    def fill_username(self, data):
        """Set the user name from the given data. """
        check_input_params(data, self.USERNAME)
        self.username = data[self.USERNAME]

    def fill_password(self, data):
        """Set the user password from the given data. """
        check_input_params(data, self.PASSWORD)
        self.password = data[self.PASSWORD]

    def __init__(self, data):
        self.fill_username(data)
        self.fill_password(data)

    def get_params(self):
        """Return the user parameters as a dictionary. """
        return {
            'username': self.username,
            'password': self.password
        }
