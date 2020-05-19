"""Module for the http request classes. """

import BaseHTTPServer
import json

from activities_python.common.models.response import ControllerResponse
from activities_python.constants.basic_constants import BasicConstants


class WebRequestHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    """Handler for HTTP requests. """

    GET_METHOD = BasicConstants.GET
    POST_METHOD = BasicConstants.POST

    def do_GET(self):  # pylint: disable=invalid-name
        """Handle an http GET request. """
        self.handle_method(self.GET_METHOD)

    def do_POST(self):  # pylint: disable=invalid-name
        """Handle an http POST request. """
        self.handle_method(self.POST_METHOD)

    def get_payload(self, max_size):
        """Return the payload from the request input stream. """
        # pylint: disable=protected-access
        self.rfile._sock.settimeout(self.server.options.read_timeout_milliseconds/1000)
        payload_len = int(self.headers.getheader(BasicConstants.CONTENT_LENGTH, 0))
        payload_len = min(payload_len, max_size)
        payload = self.rfile.read(payload_len)
        return payload

    def handle_method(self, method):
        """Handle the given method type. """
        # pylint: disable=protected-access
        self.wfile._sock.settimeout(self.server.options.write_timeout_milliseconds/1000)
        controller = self.server.routes_repo.get_controller(method, self.path, self.server.options)
        data = None
        if method == self.POST_METHOD:
            data = self.get_payload(self.server.options.max_request_size)
        result = controller.handle(data, None)
        if result.jsonize:
            result = ControllerResponse(
                response=json.dumps(result.response),
                status=result.status,
                mime=result.mime
            )
        self.send_response(result.status)
        self.send_header(BasicConstants.CONTENT_TYPE, result.mime)
        self.end_headers()
        self.wfile.write(result.response)
