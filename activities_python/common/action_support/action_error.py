"""Module for action errors. """


class ActionError(Exception):
    """Class representing an Action error. """

    def __init__(self, code, message):
        super(ActionError, self).__init__(message)
        self.code = code
