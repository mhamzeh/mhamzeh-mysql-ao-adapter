"""Module for health check controller classes. """

from activities_python.common.controllers.base import BaseController
from activities_python.common.factories.logger import produce_logger
from activities_python.common.models.response import ControllerResponse


class HealthController(BaseController):
    """Controller for the health check path. """

    def __init__(self, options):
        self.logger = produce_logger(options)

    def handle(self, data, context):
        """Handle the incoming request to this controller. """
        return ControllerResponse(response='I am good!')
