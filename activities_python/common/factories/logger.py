"""Module for adapter logging. """

import logging


def produce_logger(options):
    """Return a new logger instance. """
    logging.basicConfig(level=logging.getLevelName(options.log_level))
    return logging.getLogger(__name__)
