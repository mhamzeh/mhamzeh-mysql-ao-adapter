"""Module for the base controller. """
import abc
import six


@six.add_metaclass(abc.ABCMeta)
class BaseController(object):
    """The Base Controller class. """

    @abc.abstractmethod
    def handle(self, data, context):
        """Handle the incoming request to this controller. """
        pass
