import argparse

from gwpycore import basic_cli_parser

# TODO Move this to __init__.py
__version__ = "2.0.3"

# KEEP IN MIND: logging has not been set up yet. Don't try to make logging calls in here.


def parse_args(args) -> argparse.Namespace:
    """Parse any command line parameters.

    Args:
      args ([str]): command line parameters as a list of strings

    Returns:
      An object of type argparse.Namespace.  Access the settings as object attributes (e.g. switches.logfile).

    Note: --version and --help are handled immediately as they are parsed.
      In both cases, parse_args will raise a SystemExit exception
    """
    parser = basic_cli_parser(version_text=__version__, verbose=True, very_verbose=True, nocolor=True, devel=True, trace=True, configfile_default="./local/radiolog.ini", logfile_default="RadioLog_log.txt")
    parser.add_argument("-m", "--min", dest="minmode", help="minimum display size mode enabled", action="store_true", default=False)
    parser.add_argument("--nosend", dest="nosend", help="will not send any GET requests for this session", action="store_true", default=False)
    parser.add_argument("--nologfile", dest="nologfile", help="suppresses using a log file, relying on just the console", action="store_true", default=False)

    return parser.parse_args(args)
