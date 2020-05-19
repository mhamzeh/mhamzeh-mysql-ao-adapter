"""Module for basic constants. """


class BasicConstants(object):
    """Class to encapsulate commonly used constants. """

    GET = 'GET'
    POST = 'POST'
    HTTP = 'http'
    HTTPS = 'https'
    CONTENT_TYPE = 'Content-Type'
    CONTENT_LENGTH = 'content-length'
    CONTENT_TYPE_VALUE = 'application/json'

    VERIFY_TARGET_URL = '/api/v2/authtoken/'

    TARGET = 'target'
    ACTIVITY = 'activity'

    ACTIVITY_1_NAME = 'hello_world'
    ACTIVITY_2_NAME = 'create_template'
    ACTIVITY_3_NAME = 'run_script'
    ACTIVITY_1_URL = '/api/v2/get_template/'
    ACTIVITY_2_URL = '/api/v2/create_template/'
    TARGET_NAME = 'endpoint'
    ACTIVITY_1_TYPE = ACTIVITY + '.' + ACTIVITY_1_NAME
    ACTIVITY_2_TYPE = ACTIVITY + '.' + ACTIVITY_2_NAME
    ACTIVITY_3_TYPE = ACTIVITY + '.' + ACTIVITY_3_NAME
    VERIFY_TARGET_TYPE = TARGET + '.' + TARGET_NAME

    def __init__(self):
        pass
