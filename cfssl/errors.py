"""The errors module defines an exception for CFSSL."""

class ResponseFailure(Exception):
    """A ResponseFailure is an API failure."""

    def __init__(self, msg):
        """Create an exception with the given message."""
        print msg
        msg = msg['message'] + ' (CFSSL error ' + str(msg['code']) + ')'
        Exception.__init__(self, msg)

class HTTPError(Exception):
    """An HTTPError is an HTTP non-200 failure."""

    def __init__(self, code):
        """Create an exception with the given message."""
        msg = 'server returned status code ' + str(code)
        Exception.__init__(self, msg)

