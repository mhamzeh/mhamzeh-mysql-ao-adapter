"""Module for server use cases. """

import ssl

from activities_python.common.factories.logger import produce_logger
from activities_python.common.factories.options import produce_options
from activities_python.common.http.web_request import WebRequestHandler
from activities_python.common.http.web_server import WebServer
from activities_python.common.repositories.routes import RoutesRepository


class ServerUseCase(object):
    """Class representing the Server use case. """

    def __init__(self):
        self.logger = None

    def execute(self):
        """Execute this use case. """
        opts = produce_options(False)
        self.logger = produce_logger(opts)
        try:
            self.logger.info('Options %s', str(opts.__dict__))
            opts.validate()
            routes_repo = RoutesRepository()
            http_server = WebServer(routes_repo, opts, ('', opts.port), WebRequestHandler)

            if opts.cert_file == "" or opts.pkey_file == "":
                self.logger.exception("Failed to start server, missing certs")
                exit()

            http_server.socket = ssl.wrap_socket(
                http_server.socket,
                certfile=opts.cert_file,
                keyfile=opts.pkey_file,
                ca_certs=opts.ca_file,
                cert_reqs=ssl.CERT_OPTIONAL,
                server_side=True,
                ssl_version=ssl.PROTOCOL_TLSv1_2
            )
            self.logger.info('Starting HTTP server at port %d', opts.port)

            try:
                http_server.serve_forever()
            except KeyboardInterrupt:
                pass
            self.logger.info('Stopping HTTP server')
            http_server.server_close()
        except ValueError:
            self.logger.exception("Value error")
            exit()
