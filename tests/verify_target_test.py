import logging
import responses
import unittest

from activities_python.actions.verify_target import VerifyTargetQuery
from activities_python.common.action_support.action_error import ActionError


class TestVerifyTarget(unittest.TestCase):

    def test_verify_target(self):
        query = VerifyTargetQuery()
        query.logger = logging.getLogger()
        return query

    def test_empty(self):
        query = self.test_verify_target()
        with self.assertRaises(ActionError):
            query.invoke({}, {})

    @responses.activate
    def test_good(self):
        responses.add(responses.POST, 'http://domain.com:8234/api/v2/authtoken/',
                      json={'token': 'test'}, status=200)
        query = self.test_verify_target()
        query.proxies = {}
        result = query.invoke({
            "username": "u1",
            "password": "p1",
            "host": "domain.com",
            "port": 8234
        }, {})
        self.assertEquals({"verified": True}, result)

    @responses.activate
    def test_good_with_proxy(self):
        responses.add(responses.POST, 'http://domain.com:8234/api/v2/authtoken/',
                      json={'token': 'test'}, status=200)
        query = self.test_verify_target()
        query.proxies = {
            'http': 'http://domain.com:3128',
            'https': 'http://domain.com:3128',
        }
        result = query.invoke({
            "username": "u1",
            "password": "p1",
            "host": "domain.com",
            "port": 8234
        }, {})
        self.assertEqual({"verified": True}, result)

    @responses.activate
    def test_bad(self):
        responses.add(responses.POST, 'https://domain.com/api/v2/authtoken/',
                      json={"token": None}, status=200)
        query = self.test_verify_target()
        with self.assertRaises(ActionError):
            query.invoke({
                "username": "u1",
                "password": "p1",
                "host": "domain.com",
                "protocol": "https"
            }, {})

    @responses.activate
    def test_error(self):
        responses.add(responses.POST, 'https://domain.com/api/v2/authtoken/',
                      json={"token": None}, status=403)
        query = self.test_verify_target()
        with self.assertRaises(ActionError):
            query.invoke({
                "username": "u1",
                "password": "p1",
                "host": "domain.com",
                "protocol": "https"
            }, {})

    @responses.activate
    def test_empty_token(self):
        responses.add(responses.POST, 'https://domain.com/api/v2/authtoken/',
                      json={}, status=200)
        query = self.test_verify_target()
        with self.assertRaises(ActionError):
            query.invoke({
                "username": "u1",
                "password": "p1",
                "host": "domain.com",
                "protocol": "https"
            }, {})

    @responses.activate
    def test_connection_error(self):
        query = self.test_verify_target()
        with self.assertRaises(ActionError):
            query.invoke({
                "username": "u1",
                "password": "p1",
                "host": "domain.com",
                "protocol": "https"
            }, {})


if __name__ == '__main__':
    unittest.main()
