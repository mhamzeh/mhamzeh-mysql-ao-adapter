import unittest

from activities_python.pythonutils.utils import dump_excluding_secrets, create_proxies, get_proxies, bypass_proxies
from activities_python.common.action_support.action_error import ActionError


class TestDumpExcludingSecrets(unittest.TestCase):
    lh_options = {
        "secure_keys": ["password", "key", "credentials.password", "credentials3.credentials.password"]
    }
    event = {
        "password": "secret",
        "credentials": {
            "password": "secret2"
        },
        "credentials3": {
            "credentials": {
                "password": "secret3"
            }
        },
        "key": "key",
    }

    def test_all(self):
        dump = dump_excluding_secrets(self.event, self.lh_options)
        expected = {
            "password": "*****",
            "credentials": {
                "password": "*****"
            },
            "credentials3": {
                "credentials": {
                    "password": "*****"
                }
            },
            "key": "*****",
        }
        self.assertEquals(expected, dump)

    def test_part1(self):
        lh_options = {
            "secure_keys": ["key", "credentials3.credentials.password"]
        }
        dump = dump_excluding_secrets(self.event, lh_options)
        expected = {
            "password": "secret",
            "credentials": {
                "password": "secret2"
            },
            "credentials3": {
                "credentials": {
                    "password": "*****"
                }
            },
            "key": "*****",
        }
        self.assertEquals(expected, dump)

    def test_empty_keys(self):
        lh_options = {
            "secure_keys": []
        }
        dump = dump_excluding_secrets(self.event, lh_options)
        self.assertEquals(self.event, dump)

    def test_empty_options(self):
        lh_options = {}
        dump = dump_excluding_secrets(self.event, lh_options)
        self.assertEquals(self.event, dump)

    def test_wrong_keys(self):
        lh_options = {
            "secure_keys": ["passwd", "cred.password"]
        }
        dump = dump_excluding_secrets(self.event, lh_options)
        self.assertEquals(self.event, dump)

    def test_wrong_and_correct_keys(self):
        lh_options = {
            "secure_keys": ["passwd", "credentials3.credentials.password"]
        }
        dump = dump_excluding_secrets(self.event, lh_options)
        expected = {
            "password": "secret",
            "credentials": {
                "password": "secret2"
            },
            "credentials3": {
                "credentials": {
                    "password": "*****"
                }
            },
            "key": "key",
        }
        self.assertEquals(expected, dump)


class TestCreateProxies(unittest.TestCase):

    def test_all(self):
        ops = {}
        ops['http_proxy'] = {}
        ops['https_proxy'] = {}
        ops['http_proxy']['url'] = "http://domain.com:3128"
        ops['http_proxy']['username'] = "proxyclient"
        ops['http_proxy']['password'] = "proxypassword"
        ops['https_proxy']['url'] = "http://domain.com:3128"
        ops['https_proxy']['username'] = "proxyclient"
        ops['https_proxy']['password'] = "proxypassword"
        ops['bypass_list'] = "*.cisco.com"

        dump = create_proxies(ops)
        expected = {
            'http': 'http://proxyclient:proxypassword@domain.com:3128',
            'https': 'http://proxyclient:proxypassword@domain.com:3128',
            'no_proxy': "*.cisco.com"
        }
        self.assertEquals(expected, dump)

    def test_empty_username(self):
        ops = {}
        ops['http_proxy'] = {}
        ops['https_proxy'] = {}
        ops['http_proxy']['url'] = "http://domain.com:3128"
        ops['http_proxy']['username'] = ""
        ops['http_proxy']['password'] = ""
        ops['https_proxy']['url'] = "http://domain.com:3128"
        ops['https_proxy']['username'] = ""
        ops['https_proxy']['password'] = ""
        ops['bypass_list'] = "*.cisco.com"
        dump = create_proxies(ops)
        expected = {
            'http': 'http://domain.com:3128',
            'https': 'http://domain.com:3128',
            'no_proxy': "*.cisco.com"
        }
        self.assertEquals(expected, dump)

    def test_empty_bypass_list(self):
        ops = {}
        ops['http_proxy'] = {}
        ops['https_proxy'] = {}
        ops['http_proxy']['url'] = "http://domain.com:3128"
        ops['https_proxy']['url'] = "http://domain.com:3128"
        dump = create_proxies(ops)
        expected = {
            'http': 'http://domain.com:3128',
            'https': 'http://domain.com:3128'
        }
        self.assertEquals(expected, dump)

    def test_empty_http(self):
        ops = {}
        ops['https_proxy'] = {}
        ops['https_proxy']['url'] = "http://domain.com:3128"
        dump = create_proxies(ops)
        expected = {
            'http': 'http://domain.com:3128',
            'https': 'http://domain.com:3128'
        }
        self.assertEquals(expected, dump)

    def test_empty_proxies(self):
        proxy_options = {}
        dump = create_proxies(proxy_options)
        expected = {}
        self.assertEquals(expected, dump)

    def test_parse_error(self):
        ops = {}
        ops['http_proxy'] = {}
        ops['https_proxy'] = {}
        ops['http_proxy']['url'] = "domain.com:3128"
        ops['https_proxy']['url'] = "domain.com:3128"
        with self.assertRaises(ActionError) as context:
            create_proxies(ops)
        self.assertEqual("Parse proxy url error", str(context.exception))


class TestGetProxies(unittest.TestCase):

    def test_all(self):
        proxies = {
            'http': 'http://domain.com:3128',
            'https': 'http://domain.com:3128',
            'no_proxy': "*.cisco.com"
        }

        url = "https://test.cisco.com"
        dump = get_proxies(proxies, url)
        expected = None
        self.assertEquals(expected, dump)

        url = "https://test.domain.com"
        dump = get_proxies(proxies, url)
        self.assertEquals(proxies, dump)


class TestBypassProxies(unittest.TestCase):

    def test_all(self):

        no_proxy = "10.11.12.13:8080"
        url = "http://10.11.12.13:8080"
        dump = bypass_proxies(url, no_proxy)
        self.assertEquals(True, dump)

        no_proxy = "*"
        url = "https://test.cisco.com"
        dump = bypass_proxies(url, no_proxy)
        self.assertEquals(True, dump)

        no_proxy = "*.cisco.com"
        url = "https://test.cisco.com"
        dump = bypass_proxies(url, no_proxy)
        self.assertEquals(True, dump)

        no_proxy = "10.11.38.0/24"
        url = "https://10.11.38.13"
        dump = bypass_proxies(url, no_proxy)
        self.assertEquals(True, dump)

        no_proxy = "10.11.38.13"
        url = "https://10.11.38.13"
        dump = bypass_proxies(url, no_proxy)
        self.assertEquals(True, dump)

        no_proxy = ".cisco.com"
        url = "https://test.cisco.com"
        dump = bypass_proxies(url, no_proxy)
        self.assertEquals(True, dump)

        no_proxy = "*cisco.com"
        url = "https://test.cisco.com"
        dump = bypass_proxies(url, no_proxy)
        self.assertEquals(True, dump)

        no_proxy = "cisco.com"
        url = "https://test.cisco.com"
        dump = bypass_proxies(url, no_proxy)
        self.assertEquals(False, dump)

        no_proxy = "domain.com, cisco.com"
        url = "https://test.cisco.com"
        dump = bypass_proxies(url, no_proxy)
        self.assertEquals(False, dump)

        no_proxy = ""
        url = "https://test.cisco.com"
        dump = bypass_proxies(url, no_proxy)
        self.assertEquals(False, dump)

        no_proxy = "domain.net:8080"
        url = "http://domain.net:8080"
        dump = bypass_proxies(url, no_proxy)
        self.assertEquals(True, dump)


if __name__ == '__main__':
    unittest.main()
