import os
from app.db.file_management import determine_rotate_method
from dataclasses import dataclass
from app.logic.mapping import Datum, CoordFormat
from pathlib import Path
import argparse, configparser
from app.logic.exceptions import  RadioLogConfigError, RadioLogConfigSettingWarning
import logging

LOG = logging.getLogger("main")

DEFAULT_NAME = 'Search and Rescue'
DEFAULT_LOGO = 'radiolog_logo.jpg'
DEFAULT_CLUE_REPORT = 'clueReportFillable.pdf'
DEFAULT_TIMEOUT = 30
DEFAULT_WORKINGDIR = 'testdata'
DEFAULT_SARSOFT_SERVER = "localhost"

def _as_path(input: str) -> Path:
    return Path(input)

def _as_datum(input: str) -> Datum:
    return Datum.__members__[input]

def _as_coordFormat(input: str) -> CoordFormat:
    return CoordFormat.__members__[input]

CONVERTERS = {
    'path': _as_path,
    'datum': _as_datum,
    'coordformat': _as_coordFormat
}


def __agency_section(parser, config):
    config.agencyName = DEFAULT_NAME
    config.logo = Path(DEFAULT_LOGO)
    if parser.has_section('agency'):
        config.agencyName = parser.get('agency', 'name', fallback=config.agencyName)
        config.logo = parser['agency'].getpath('logo', config.logo)

def __storage_section(parser, config):
    config.firstWorkingDir = Path(DEFAULT_WORKINGDIR)
    config.secondWorkingDir = None
    (config.rotateScript, config.rotateDelimiter) = determine_rotate_method()

    if parser.has_section('storage'):
        config.firstWorkingDir = parser['storage'].getpath('firstworkingdir', config.firstWorkingDir)
        config.secondWorkingDir = parser['storage'].getpath('secondworkingdir', config.secondWorkingDir)
        config.rotateScript = parser.get('storage', "rotateScript", fallback=config.rotateScript)
        config.rotateDelimiter = parser.get('storage', "rotateDelimiter", fallback=config.rotateDelimiter)

def __display_section(parser, config):
    config.timeoutMinutes = DEFAULT_TIMEOUT  # initial timeout interval (valid: 10..120 step 10)
    if parser.has_section('display'):
        config.timeoutMinutes = parser['display'].getint('timeoutminutes', config.timeoutMinutes)

def __tabgroups_section(parser, config):
    config.tabGroups = []
    if parser.has_section('tabgroups'):
        config.tabGroups = []
        for (tabName,tabRE) in parser['tabgroups'].items():
            config.tabGroups.append(tabRE)

def __reports_section(parser, config):
    config.clueReport = Path(DEFAULT_CLUE_REPORT)
    if parser.has_section('reports'):
        config.clueReport = parser['reports'].getpath('cluereport', config.clueReport)

def __mapping_section(parser, config, issues):
    config.datum = Datum.WGS84
    config.coordFormat = CoordFormat.UTM7
    if parser.has_section('mapping'):
        try:
            config.datum = parser['mapping'].getdatum('datum', config.datum)
        except KeyError as e:
            issues.append(RadioLogConfigSettingWarning("[mapping]datum", e.args[0], Datum.possibleValues()))

        try:
            config.coordFormat = parser['mapping'].getcoordformat('coordformat', config.coordFormat)
        except KeyError as e:
            issues.append(RadioLogConfigSettingWarning("[mapping]coordformat", e.args[0], CoordFormat.possibleValues()))

def __interop_section(parser, config, issues):
    config.sarsoftServerName = DEFAULT_SARSOFT_SERVER
    if parser.has_section('interop'):
        config.sarsoftServerName = parser.get('RadioLog', "server")

def load_config(filename: str = "", ini: str = "", config: argparse.Namespace = None) -> argparse.Namespace:
    """
    Parse the contents of the config (INI) file.

    Args:
      filename -- the name of the file to be parsed, or...
      ini -- the actual text to be parsed
      config (optional) -- An existing argparse.Namespace to be appended to

    Returns:
      An object of type argparse.Namespace. Access the settings as object attributes (e.g. config.datum).
    """
    LOG.trace("Loading config")
    parser = configparser.ConfigParser(converters=CONVERTERS)
    if filename:
        parser.read_file(open(filename,encoding="UTF-8"))
    else:
        parser.read_string(ini)

    if not config:
        config = argparse.Namespace()

    issues = []
    __agency_section(parser, config)
    __display_section(parser, config)
    __tabgroups_section(parser, config)
    __reports_section(parser, config)
    __mapping_section(parser, config, issues)
    __storage_section(parser, config)
    __interop_section(parser, config, issues)

    for issue in issues:
        LOG.exception(issue)

    LOG.debug(f"config = {config}")
    return config

__all__ = ("load_config")


