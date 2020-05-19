import logging
import responses
import unittest

from activities_python.actions.action_create_template import ActionQuery2
from activities_python.common.action_support.action_error import ActionError


class TestJobTemplateListTest(unittest.TestCase):

    def get_job_template_launch_query(self):
        query = ActionQuery2()
        query.logger = logging.getLogger()
        return query

    def test_empty(self):
        query = self.get_job_template_launch_query()
        with self.assertRaises(ActionError):
            query.invoke({}, {})

    @responses.activate
    def test_good(self):
        responses.add(responses.POST, 'http://domain.com:8234/api/v2/authtoken/',
                      json={'token': 'test'}, status=200)
        responses.add(responses.POST, 'http://domain.com:8234/api/v2/create_template/name',
                      json={"info": "result"}, status=200)
        query = self.get_job_template_launch_query()
        query.proxies = {}
        result = query.invoke({
            "username": "u1",
            "password": "p1",
            "host": "domain.com",
            "port": 8234,
            "template_name": "name",
            "credential": "1"
        }, {})
        self.assertEqual({"info": "result"}, result)

    @responses.activate
    def test_good_with_proxy(self):
        responses.add(responses.POST, 'http://domain.com:8234/api/v2/authtoken/',
                      json={'token': 'test'}, status=200)
        responses.add(responses.POST, 'http://domain.com:8234/api/v2/create_template/name',
                      json={"info": "result"}, status=200)
        query = self.get_job_template_launch_query()
        query.proxies = {
            'http': 'http://domain.com:3128',
            'https': 'http://domain.com:3128',
        }
        result = query.invoke({
            "username": "u1",
            "password": "p1",
            "host": "domain.com",
            "port": 8234,
            "template_name": "name",
            "credential": "1"
        }, {})
        self.assertEqual({"info": "result"}, result)

    @responses.activate
    def test_bad(self):
        responses.add(responses.POST, 'http://domain.com:8234/api/v2/authtoken/',
                      json={'token': 'test'}, status=200)
        responses.add(responses.POST, 'http://domain.com:8234/api/v2/create_template/name',
                      json={"info": "result"}, status=403)
        query = self.get_job_template_launch_query()
        with self.assertRaises(ActionError):
            query.invoke({
                "username": "u1",
                "password": "p1",
                "host": "domain.com",
                "port": 8234,
                "template_name": "name",
                "credential": "1",
            }, {})

    @responses.activate
    def test_bad2(self):
        responses.add(responses.POST, 'http://domain.com:8234/api/v2/authtoken/',
                      json={'token': 'test'}, status=200)
        query = self.get_job_template_launch_query()
        with self.assertRaises(ActionError):
            query.invoke({
                "username": "u1",
                "password": "p1",
                "host": "domain.com",
                "port": 8234,
                "template_name": "name",
                "credential": "1",
            }, {})


if __name__ == '__main__':
    unittest.main()
