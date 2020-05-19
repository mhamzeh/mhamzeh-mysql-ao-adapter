"""Module for various utilities. """

import copy

from urlparse import urlparse
from requests.utils import is_ipv4_address, is_valid_cidr, address_in_network

from activities_python.common.action_support.action_error import ActionError
from activities_python.pythonutils.template_error import TemplateError


def get_optional_value(data, key, default):
    """Return the value for the given option, or the provided default value. """
    if key in data:
        result = data[key]
    else:
        result = default
    return result


def check_input_params(data, param):
    """Verify the data contains the required input parameter, or raise an error. """
    if param not in data:
        raise_action_error(400, param + ' field is required')


def check_reponse_params(data, param):
    """Verify the data contains the required response parameter, or raise an error. """
    if param not in data:
        raise TemplateError(503, "No " + param + " in response", data)


def raise_action_error(code, message):
    """Raise an ActionError with the specified code and error message. """
    raise ActionError(code, message)


def dump_excluding_secrets(event, lh_options):
    """Function to dump incoming event excluding secrets."""
    if not isinstance(event, dict) or not isinstance(lh_options, dict):
        return event
    if 'secure_keys' not in lh_options:
        return event
    dump_event = copy.deepcopy(event)
    secure_keys = lh_options['secure_keys']
    if isinstance(secure_keys, (list, tuple)):
        return exclude_secrets_from_list(secure_keys, dump_event)
    elif isinstance(secure_keys, str):
        if secure_keys != "":
            dump_event[secure_keys] = "*****"
        return dump_event
    else:
        return event


def exclude_secrets_from_list(secure_keys, dump_event):
    """Function to dump incoming event excluding secrets from list or tuple."""
    for key in secure_keys:
        if key == "":
            continue
        obj = dump_event
        split_key_list = key.split(".")
        if len(split_key_list) == 1:
            if key in obj:
                obj[key] = "*****"
        else:
            wrong = False
            for i, var in enumerate(split_key_list):
                if i < len(split_key_list) - 1:
                    if var in obj:
                        obj = obj[var]
                    else:
                        wrong = True
                        break
            if not wrong:
                path = split_key_list[-1]
                if path in obj:
                    obj[path] = "*****"
    return dump_event


def create_proxies(proxy_options):
    """Function to create a proxies object from suite admin proxy configuration."""
    proxies = {}
    http_proxy = proxy_options.get('http_proxy', None)
    if http_proxy:
        http_proxy_url = create_proxy_url(http_proxy.get('url', ""), http_proxy.get('username', ""),
                                          http_proxy.get('password', ""))
        if http_proxy_url != "":
            proxies['http'] = http_proxy_url
            proxies['https'] = http_proxy_url
    https_proxy = proxy_options.get('https_proxy', None)
    if https_proxy:
        https_proxy_url = create_proxy_url(https_proxy.get('url', ""), https_proxy.get('username', ""),
                                           https_proxy.get('password', ""))
        if https_proxy_url != "":
            proxies['https'] = https_proxy_url
            if 'http' not in proxies:
                proxies['http'] = https_proxy_url
    no_proxy = proxy_options.get('bypass_list', "")
    if no_proxy != "":
        proxies['no_proxy'] = no_proxy
    return proxies


def create_proxy_url(url, username, password):
    """Function to create a proxy url."""
    if url == "":
        return ""
    parse_url = urlparse(url)
    if not parse_url.scheme and not parse_url.netloc:
        raise_action_error(400, "Parse proxy url error")
    proxy_url = url
    if username != "":
        proxy_url = parse_url.scheme + "://" + username + ":" + password + "@" + parse_url.netloc
    return proxy_url


def bypass_proxies(url, no_proxy):
    """Returns whether we should bypass proxies or not."""
    parsed = urlparse(url)
    bypass = False
    if no_proxy == "":
        return False
    no_proxy = (
        host for host in no_proxy.replace(' ', '').split(',') if host
    )
    host_with_port = parsed.hostname
    if parsed.port:
        host_with_port += ':{0}'.format(parsed.port)
    chars = ("*", "*.", ".")
    for host in no_proxy:
        if host == "*":
            bypass = True
        if host == parsed.hostname or host == host_with_port:
            bypass = True
        if host.startswith(chars):
            host = host.lstrip('*')
            host = host.lstrip('.')
            if parsed.hostname.endswith(host) or host_with_port.endswith(host):
                bypass = True
        if is_ipv4_address(parsed.hostname):
            if is_valid_cidr(host):
                if address_in_network(host_with_port, host):
                    bypass = True
    return bypass


def get_proxies(proxies, url):
    """Returns proxies. If url in proxy bypass list, returns None."""
    if proxies and 'no_proxy' in proxies:
        no_proxy = proxies['no_proxy']
        if no_proxy:
            if bypass_proxies(url, no_proxy):
                return None
    return proxies
