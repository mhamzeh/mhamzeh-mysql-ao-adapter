"""Module for the http server classes. """

import BaseHTTPServer


class WebServer(BaseHTTPServer.HTTPServer):
    """Class representing an http server. """

    def __init__(self, routes_repo, options, *args, **kw):
        self.timeout = options.timeout_milliseconds/1000
        BaseHTTPServer.HTTPServer.__init__(self, *args, **kw)
        self.routes_repo = routes_repo
        self.options = options
