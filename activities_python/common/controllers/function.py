"""Module for the Function controller classes. """

import json
import six

from activities_python.common.action_support.action_error import ActionError
from activities_python.common.constants.controller import ControllerConstants
from activities_python.common.controllers.base import BaseController
from activities_python.common.factories.logger import produce_logger
from activities_python.common.models.response import ControllerResponse
from activities_python.constants.basic_constants import BasicConstants
from activities_python.events.event_resolver import resolve_event
from activities_python.pythonutils.utils import dump_excluding_secrets, create_proxies


class FunctionController(BaseController):
    """Controller for the Functions path. """

    def __init__(self, options):
        self.options = options
        self.logger = produce_logger(options)

    def handle(self, data, context):
        """Handle the incoming request to this controller. """
        # pylint: disable=broad-except
        try:
            if isinstance(data, six.string_types):
                input_object = json.loads(data)
            else:
                input_object = data
            input_type = input_object['type']
            self.logger.info("Got event type %s", input_type)
            lh_options = {}
            proxy_options = {}
            no_proxy = False
            if 'lh_options' in input_object:
                lh_options = input_object['lh_options']
                if lh_options and 'proxy_options' in lh_options:
                    proxy_options = lh_options['proxy_options']
            event = input_object['config']
            self.logger.info("Got event config %s", dump_excluding_secrets(event, lh_options))
            handler = resolve_event(input_type, self.options)
            if not handler:
                raise ValueError("Unresolved event type: " + input_type)
            handler.add_lh_options(lh_options)
            if 'no_proxy' in event:
                no_proxy = event['no_proxy']
            if proxy_options and not no_proxy:
                proxies = create_proxies(proxy_options)
                if proxies:
                    handler.add_proxies(proxies)
            result = handler.invoke(event, context)
            return self.__action_success(result)
        except ActionError as e:
            self.logger.error("Raised action error code=%s, message=%s", e.code, e)
            return self.__action_error(str(e), e.code)
        except Exception as e:
            self.logger.exception("Exception during processing request")
            return self.__action_error(str(e), None)

    def __action_success(self, result):
        response = {
            ControllerConstants.ACTIVITY_STATUS: ControllerConstants.SUCCESS_STATUS,
        }
        if result:
            response[ControllerConstants.RESPONSE] = result
        return self.__create_response(response)

    def __action_error(self, error_text, code):
        response = {
            ControllerConstants.ACTIVITY_STATUS: ControllerConstants.FAILED_STATUS,
            ControllerConstants.ERROR_DESC: {
                ControllerConstants.ERROR_MESSAGE: error_text,
            }
        }
        if code:
            response[ControllerConstants.ERROR_DESC][ControllerConstants.ERROR_CODE] = str(code)
        return self.__create_response(response)

    @staticmethod
    def __create_response(result):
        return ControllerResponse(
            response=result,
            status=200,
            mime=BasicConstants.CONTENT_TYPE_VALUE,
            jsonize=True,
        )
