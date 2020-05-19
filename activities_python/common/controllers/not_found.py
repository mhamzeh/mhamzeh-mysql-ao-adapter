"""Module for the not-found controller. """

from activities_python.common.controllers.base import BaseController
from activities_python.common.factories.logger import produce_logger
from activities_python.common.models.response import ControllerResponse


class NotFoundController(BaseController):
    """Controller for handling requests to invalid paths. """

    def __init__(self, options):
        self.logger = produce_logger(options)

    def handle(self, data, context):
        """Handle incoming requests to this controller. """
        return ControllerResponse(status=404)
