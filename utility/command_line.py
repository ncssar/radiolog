import argparse

__version__ = "2.0.2"

# KEEP IN MIND: logging has not been set up yet. Don't try to make logging calls in here.


def parse_args(args):
    """Parse any command line parameters.

    Args:
      args ([str]): command line parameters as a list of strings

    Returns:
      An object of type argparse.Namespace.  Access the settings as object attributes (e.g. switches.logfile).

    Note: --version and --help are handled immediately as they are parsed.
      In both cases, parse_args will raise a SystemExit exception
    """
    parser = argparse.ArgumentParser(description="")
    parser.add_argument("--version", action="version", version=f"RadioLog version {__version__}")
    parser.add_argument("-m", "--min", dest="minmode", help="minimum display size mode enabled", action="store_true", default=False)
    parser.add_argument("--nosend", dest="nosend", help="will not send any GET requests for this session", action="store_true", default=False)
    parser.add_argument("-d", "--devel", dest="devmode", help="turns on developer mode", action="store_true", default=False)
    parser.add_argument("-v", "--verbose", dest="loglevel", help="sets loglevel to DIAGNOSTIC", action="store_const", const=DIAGNOSTIC, default=INFO)
    parser.add_argument("--debug", dest="loglevel", help="sets loglevel to DEBUG (very verbose)", action="store_const", const=DEBUG)
    parser.add_argument("--trace", dest="loglevel", help="sets loglevel to TRACE (super verbose)", action="store_const", const=TRACE)
    parser.add_argument("--nocolor", dest="nocolor", help="turns off coloring the log messages that are sent to the console", action="store_true", default=False)
    parser.add_argument("-l", "--logfile", dest="logfile", help="specifies the name (and path) for the log file (RadioLog_log.txt by default)", default="RadioLog_log.txt")
    parser.add_argument("--nologfile", dest="nologfile", help="suppresses using a log file, relying on just the console", action="store_true", default=False)
    parser.add_argument("-c", "--configfile", dest="configfile", help="specifies the name (and path) for the configuration file (instead of ./local/radiolog.cfg)", default="./local/radiolog.cfg")

    return parser.parse_args(args)
