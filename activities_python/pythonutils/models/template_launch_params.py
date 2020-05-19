"""Module for the adapter launch parameters. """


class TemplateLaunchParams(object):
    """Class representing the adapter launch parameters. """

    EXTRA_VARS = "extra_vars"

    def __init__(self, data):
        self.param_names = [
            self.EXTRA_VARS,
        ]
        self.params = {}
        for param in self.param_names:
            if param in data:
                self.params[param] = data[param]

    def get_params(self):
        """Return the adapter launch parameters dictionary. """
        return self.params
