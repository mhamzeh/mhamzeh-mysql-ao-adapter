"""Module containting the template adapter classes.  """

import requests

from requests import ConnectionError
from requests import ConnectTimeout
from requests import HTTPError
from requests import ReadTimeout
from requests import Timeout

from activities_python.constants.basic_constants import BasicConstants
from activities_python.pythonutils.models.template_token import TemplateToken
from activities_python.pythonutils.template_error import TemplateError
from .utils import get_proxies

class TemplateAdapter(object):
    """The Template Adapter class. """

    def __init__(self, target, logger):
        self.target = target
        self.logger = logger

    def get_auth_token(self, user, proxies):
        """Return the auth token for the specified user. """
        try:
            url = self.target.get_host() + BasicConstants.VERIFY_TARGET_URL
            req = requests.post(url, json=user.get_params(), verify=self.target.verify_ssl,
                                proxies=get_proxies(proxies, url))
            if req.status_code != requests.codes.ok:
                req.raise_for_status()
            self.logger.debug('get_auth_token returned ' + req.text)
            return TemplateToken(req.json())
        except HTTPError as e:
            raise TemplateError(req.status_code, str(e.message), req.text)
        except (ConnectTimeout, ReadTimeout, Timeout, ConnectionError) as e:
            raise TemplateError(503, "Connection failed", e.message)

    def get_template(self, token, template_id, proxies):
        """Return the template json for the specified template id. """
        try:
            url = self.target.get_host() + BasicConstants.ACTIVITY_1_URL + str(int(template_id))
            req = requests.get(url, headers=token.get_auth_header(), verify=self.target.verify_ssl,
                               proxies=get_proxies(proxies, url))
            if req.status_code != requests.codes.ok:
                req.raise_for_status()
            self.logger.debug('get_template returned ' + req.text)
            return req.json()
        except HTTPError as e:
            raise TemplateError(req.status_code, str(e.message), req.text)
        except (ConnectTimeout, ReadTimeout, Timeout, ConnectionError) as e:
            raise TemplateError(503, "Connection failed", e.message)

    def create_template(self, token, template_name, params, proxies):
        """Create a template for the given template name and parameters. """
        try:
            url = self.target.get_host() + BasicConstants.ACTIVITY_2_URL + template_name
            req = requests.post(url, json=params.get_params(), headers=token.get_auth_header(),
                                verify=self.target.verify_ssl, proxies=get_proxies(proxies, url))
            if req.status_code != requests.codes.ok:
                req.raise_for_status()
            self.logger.debug('create_template returned ' + req.text)
            return req.json()
        except HTTPError as e:
            raise TemplateError(req.status_code, str(e.message), req.text)
        except (ConnectTimeout, ReadTimeout, Timeout, ConnectionError) as e:
            raise TemplateError(503, "Connection failed", e.message)
