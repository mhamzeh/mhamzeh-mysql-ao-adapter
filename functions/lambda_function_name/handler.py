"""Module for Lamdba functions. """

from activities_python.common.use_cases.lambdas import LambdasUseCase


def python_activities_handler(event, context):
    """Execute the Lamdba handler for the given event. """
    return LambdasUseCase().execute(event, context)
