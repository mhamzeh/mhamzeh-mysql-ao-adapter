"""Module for the sample adapter classes. """

from activities_python.common.action_support.base import BaseAction
from activities_python.pythonutils.template_error import TemplateError
from activities_python.pythonutils.utils import check_input_params


class ActionQuery1(BaseAction):
    """Sample Class to demonstrator input and output parameters."""

    hello_world = "input_one"
    input_name = "input_two"

    output1 = "output_one"
    output2 = "output_two"

    def invoke(self, data, context):
        """Invoke this action class. """
        self.logger.info('Invoked ActionQuery1')

        check_input_params(data, self.input_name)
        output1 = data[self.input_name]

        check_input_params(data, self.hello_world)
        output2 = data[self.hello_world]

        result = {}

        try:
            result[self.output1] = output1
            result[self.output2] = output2 + output1

            return result
        except TemplateError as e:
            self.logger.error("Action failed. Status=%s, Response=%s", e.status_code, e.response)
            self.raise_action_error(e.status_code, e.message)
