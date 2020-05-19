"""Module for the adapter token."""

from activities_python.pythonutils.template_error import TemplateError
from activities_python.pythonutils.utils import check_reponse_params


class TemplateToken(object):
    """Class representing the adapter token."""

    TOKEN = "token"

    def __init__(self, responseData):
        check_reponse_params(responseData, self.TOKEN)
        if not responseData[self.TOKEN]:
            raise TemplateError(503, "empty token", "empty token")
        self.token = responseData[self.TOKEN]

    def get_auth_header(self):
        """Return the toke in the header authorization format."""
        return {'Authorization': 'Token ' + self.token}
