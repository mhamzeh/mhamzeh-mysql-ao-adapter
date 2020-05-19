"""Module for the response model. """

import collections

ControllerResponse = collections.namedtuple('ControllerResponse', ['status', 'mime', 'response', 'jsonize'])
ControllerResponse.__new__.__defaults__ = (200, 'text/plain', '', False)
