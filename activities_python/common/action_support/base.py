"""Module for action base classes. """

import abc
import six

from activities_python.common.action_support.action_error import ActionError
from activities_python.common.factories.logger import produce_logger


@six.add_metaclass(abc.ABCMeta)
class BaseAction(object):
    """Action base class. """
    logger = {}
    lh_options = {}
    proxies = {}

    def check_input_params(self, data, param):
        """Verify the data contains the given parameter, or raise an ActionError. """
        if param not in data:
            self.raise_action_error(400, param + ' field is required')

    def create_logger(self, options):
        """Create a new logger instance. """
        self.logger = produce_logger(options)
        return self

    def raise_action_error(self, code, message):
        """Raise an ActionError with the given code and error message. """
        if self.logger:
            self.logger.debug("raising action error - code: %s, message: %s", code, message)
        raise ActionError(code, message)

    def add_lh_options(self, lh_options):
        """Add the given LH Options. """
        self.lh_options = lh_options

    def add_proxies(self, proxies):
        """proxies setter."""
        self.proxies = proxies

    @abc.abstractmethod
    def invoke(self, data, context):
        """Invoke this action. """
        pass

    def __init__(self):
        self.lh_options = None
        self.logger = None
