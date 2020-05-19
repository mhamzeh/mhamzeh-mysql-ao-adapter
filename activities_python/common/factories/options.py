"""Module for the factories options. """

from activities_python.common.factories.parser import produce_parser
from activities_python.common.models.options import Options


def produce_options(is_lambda):
    """Create a new Options instance. """
    parser_obj = produce_parser()
    option_obj = Options(parser_obj)
    option_obj.load_environment(is_lambda)
    option_obj.parse_flags()
    return option_obj
