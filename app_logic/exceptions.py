class RadioLogException(Exception):
    """Base class for exceptions in this module."""
    pass


class FatalAppError(RadioLogException):
    """
    Exception raised for an insurmountable error.
    After reporting the error to the user, the app will exit with code -1.

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message):
        self.message = message
