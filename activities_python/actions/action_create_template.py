"""Module for the sample adapter classes. """

from activities_python.common.action_support.base import BaseAction
from activities_python.pythonutils.models.template_launch_params import TemplateLaunchParams
from activities_python.pythonutils.models.template_target import TemplateTarget
from activities_python.pythonutils.models.template_user import TemplateUser
from activities_python.pythonutils.template_adapter import TemplateAdapter
from activities_python.pythonutils.template_error import TemplateError
from activities_python.pythonutils.utils import check_input_params


class ActionQuery2(BaseAction):
    """Sample Class for creating some template using post request with template_name parameter."""

    TEMPLATE_NAME = "template_name"

    def invoke(self, data, context):
        """Invoke this action class. """
        self.logger.info('Invoked ActionQuery2')
        check_input_params(data, self.TEMPLATE_NAME)
        template_name = data[self.TEMPLATE_NAME]
        target = TemplateTarget(data)
        user = TemplateUser(data)
        params = TemplateLaunchParams(data)
        template_adapter = TemplateAdapter(target, self.logger)
        try:
            token = template_adapter.get_auth_token(user, self.proxies)
            info = template_adapter.create_template(token, template_name, params, self.proxies)
            return info
        except TemplateError as e:
            self.logger.error("Action failed. Status=%s, Response=%s", e.status_code, e.response)
            self.raise_action_error(e.status_code, e.message)
