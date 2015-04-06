class Error(Exception):
    """
    Base exception for manager errors.
    """

class BadConnectionIdentifier(Error, ValueError):
    """
    Exception thrown when a bad connection spec is given to a client's
    connection call.
    """

class ConnectionError(Error, IOError):
    """
    Exception thrown when a connection to the SHM failed to work as intended.
    """

class ConnectionInterrupted(ConnectionError):
    """
    Exception raised when a client's connection to the manager was interrupted
    abruptly.
    """

class ConnectionFailed(ConnectionError):
    """
    Exception raised when a client can't connect to the server.
    """
