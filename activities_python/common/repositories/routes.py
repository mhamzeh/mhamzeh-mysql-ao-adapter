"""Module for the routes repository. """

import re

from activities_python.common.controllers import function
from activities_python.common.controllers import health
from activities_python.common.controllers import not_found


class RoutesRepository(object):
    """The routes repository class. """

    PATH = 'path'
    METHOD = 'method'
    FACTORY = 'factory'

    def __init__(self):
        self.routes = [
            {
                self.PATH: r'^/api/v1/function$',
                self.METHOD: 'POST',
                self.FACTORY: lambda options, controller=function.FunctionController: controller(options)
            },
            {
                self.PATH: r'^/api/v1/healthcheck$',
                self.METHOD: 'GET',
                self.FACTORY: lambda options, controller=health.HealthController: controller(options)
            },
        ]

    def get_controller(self, method, path, options):
        """Return the controller for the given path. """
        for route in self.routes:
            if re.match(route[self.PATH], path) and route[self.METHOD] == method:
                return route[self.FACTORY](options)
        return not_found.NotFoundController(options)
