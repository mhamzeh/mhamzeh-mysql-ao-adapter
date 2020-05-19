import logging
import responses
import unittest

from activities_python.actions.action_hello_world import ActionQuery1
from activities_python.common.action_support.action_error import ActionError


class TestJobTemplateListTest(unittest.TestCase):

    def getJobTemplateLaunchInfoQuery(self):
        query = ActionQuery1()
        query.logger = logging.getLogger()
        return query

    def test_empty(self):
        query = self.getJobTemplateLaunchInfoQuery()
        with self.assertRaises(ActionError):
            query.invoke({}, {})

    @responses.activate
    def test_good(self):
        responses.add(responses.POST, 'http://domain.com:8234/api/v2/authtoken/',
                      json={'token': 'test'}, status=200)
        responses.add(responses.GET, 'http://domain.com:8234/api/v2/template/1',
                      json={"info": "result"}, status=200)
        query = self.getJobTemplateLaunchInfoQuery()
        result = query.invoke({
            "username": "u1",
            "password": "p1",
            "host": "domain.com",
            "port": 8234,
            "template_id": 1,
            "input_one": 'hello',
            "input_two": 'world'
        }, {})
        self.assertEqual({"output_one": "world", "output_two": "helloworld"}, result)

    @responses.activate
    def test_bad(self):
        responses.add(responses.POST, 'http://domain.com:8234/api/v2/authtoken/',
                      json={'token': 'test'}, status=200)
        responses.add(responses.GET, 'http://domain.com:8234/api/v2/template/1',
                      json={"info": "result"}, status=403)
        query = self.getJobTemplateLaunchInfoQuery()
        with self.assertRaises(ActionError):
            query.invoke({
                "username": "u1",
                "password": "p1",
                "host": "domain.com",
                "port": 8234,
                "template_id": 1,
            }, {})

    @responses.activate
    def test_bad2(self):
        responses.add(responses.POST, 'http://domain.com:8234/api/v2/authtoken/',
                      json={'token': 'test'}, status=200)
        query = self.getJobTemplateLaunchInfoQuery()
        with self.assertRaises(ActionError):
            query.invoke({
                "username": "u1",
                "password": "p1",
                "host": "domain.com",
                "port": 8234,
                "template_id": 1,
            }, {})


if __name__ == '__main__':
    unittest.main()
