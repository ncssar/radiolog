from utility.logger import CRITICAL, ERROR, WARNING, INFO, DIAGNOSTIC, DEBUG, TRACE

# This list of suggested exit codes is based on https://www.freebsd.org/cgi/man.cgi?query=sysexits
EX_OK = 0
# EX_WARNING = 1 # Execution completed, but there were warning(s) reported
EX_ERROR = 2  # Execution failed (with an unspecified reason)
# EX_USAGE = 64 # The command was used incorrectly (bad arguments, bad flag, etc.)
# EX_DATAERR = 65 # Bad input data
# EX_NOINPUT = 66 # Input file doesn't exist/unreadable.
# EX_NOUSER = 67
# EX_NOHOST = 68
# EX_UNAVAILABLE = 69 # A service is unavailable.
EX_SOFTWARE = 70  # An internal software error has been detected.
# EX_OSERR = 71 # An operating system error has been detected.
# EX_OSFILE = 72 # Some system file does not exist/unreadable/has syntax error.
# EX_CANTCREAT = 73 # A (user specified) output file cannot be created.
# EX_IOERR = 74 # An error occurred while doing I/O on some file.
# EX_TEMPFAIL = 75 # Temporary failure, indicating something that is not really an error.
# EX_PROTOCOL = 76 # The remote system returned something that was not possible during a protocol exchange.
# EX_NOPERM = 77 # Insufficient permission.
EX_CONFIG = 78  # Something was found in an unconfigured or miscon­figured state.


class RadioLogError(Exception):
    """
    Exception raised for a general, insurmountable error.
    Also, serves as a base-class for the more specific errors below.

    Attributes:
        message -- explanation of the error
        loglevel (optional) -- How this error should appear in the log (if no outer code catches it and handles it, that is). The default is logging.ERROR.
    """
    exitcode: int = EX_ERROR
    loglevel = ERROR

    def __init__(self, message, loglevel=ERROR):
        self.exitcode = EX_ERROR
        self.message = message
        self.loglevel = loglevel

    def __str__(self) -> str:
        return self.message


class RadioLogConfigError(RadioLogError):
    """
    Exception raised because of bad data in a config file or something wrong with our operating environment.

    Attributes:
        message -- explanation of the error(s)
        loglevel (optional) -- How this error should appear in the log (if no outer code catches it and handles it, that is). The default is logging.ERROR.
    """

    def __init__(self, message, loglevel=ERROR):
        self.exitcode = EX_CONFIG
        self.message = message
        self.loglevel = loglevel


class RadioLogConfigSettingWarning(RadioLogError):
    """
    Warning raised because of a bad setting in a config file.

    Attributes:
        key -- the name of the setting
        attempted_value -- the value that is in error
        possible_values -- (optional) a list of valid choices
        loglevel (optional) -- How this error should appear in the log (if no outer code catches it and handles it, that is). The default is logging.WARNING.
    """

    def __init__(self, key, attempted_value, possible_values=None, loglevel=WARNING):
        self.exitcode = EX_OK  # Don't exit, carry on
        self.message = f"The configuration setting of {key} = {attempted_value} is invalid."
        if possible_values:
            self.message += f" Possible values are: {possible_values}"
        self.loglevel = loglevel


__all__ = ("RadioLogError",
           "RadioLogConfigError",
           "RadioLogConfigSettingWarning")
