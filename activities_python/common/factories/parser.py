"""Module for the adapter arguments parser. """
import argparse


def produce_parser():
    """Return a new parser instance. """
    parser = argparse.ArgumentParser(description='Template Python activities adapter.')
    parser.add_argument("--log_level", dest="log_level", help="Set the logging level",
                        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'])
    parser.add_argument("-p", "--port", dest="port", help="Server `Port`", type=int)
    parser.add_argument("--cert", dest="cert_file", help="Cert File `Cert`")
    parser.add_argument("--pkey", dest="pkey_file", help="Cert File `Cert`")
    parser.add_argument("--ca", dest="ca_file", help="CA Cert File `Cert`")
    parser.add_argument("--timeout", dest="timeout_milliseconds",
                        help="Timeout in milliseconds, (10ms to 24 hours)", type=int)
    parser.add_argument("--read_timeout", dest="read_timeout_milliseconds",
                        help="Read timeout in milliseconds, (10ms to 24 hours)", type=int)
    parser.add_argument("--write_timeout", dest="write_timeout_milliseconds",
                        help="Write timeout in milliseconds, (10ms to 24 hours)", type=int)
    return parser
