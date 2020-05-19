"""Module for Lambda use cases. """

import logging

from activities_python.common.controllers.function import FunctionController
from activities_python.common.factories.options import produce_options


class LambdasUseCase(object):
    """Class presenting a Lambda use case. """

    def __init__(self):
        self.logger = None

    def execute(self, event, context):
        """Execute this use case. """
        self.logger = logging.getLogger(__name__)
        try:
            opts = produce_options(True)
            if opts.log_level:
                logging.basicConfig(level=logging.getLevelName(opts.log_level))
            controller = FunctionController(opts)
            result = controller.handle(event, context)
            return result.response
        except ValueError as e:
            self.logger.error("Value error: %s", str(e))
            exit()
