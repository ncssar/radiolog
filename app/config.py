from dataclasses import dataclass
from app.logic.mapping import Datum, CoordFormat
import utility.config_helpers
from pathlib import Path
import argparse, configparser
from app.logic.exceptions import  RadioLogConfigError, RadioLogConfigSettingWarning
import logging

LOG = logging.getLogger("RadioLog")

DEFAULT_NAME = 'Search and Rescue'
DEFAULT_LOGO = 'radiolog_logo.jpg'
DEFAULT_CLUE_REPORT = 'clueReportFillable.pdf'
DEFAULT_TIMEOUT = 30
DEFAULT_WORKINGDIR = 'testdata'

def asDatum(input: str) -> Datum:
	return Datum.__members__[input]

def asCoordFormat(input: str) -> CoordFormat:
	return CoordFormat.__members__[input]

CONVERTERS = {
	'path': utility.config_helpers.asPath,
	'datum': asDatum,
	'coordformat': asCoordFormat
}

def __agency_section(parser, config):
	config.agencyName = DEFAULT_NAME
	config.logo= Path(DEFAULT_LOGO)
	if parser.has_section('agency'):
		config.agencyName = parser.get('agency', 'name', fallback=config.agencyName)
		config.logo = parser['agency'].getpath('logo', config.logo)

def __storage_section(parser, config):
	config.firstWorkingDir = Path(DEFAULT_WORKINGDIR)
	config.secondWorkingDir = None
	if parser.has_section('storage'):
		config.firstWorkingDir = parser['storage'].getpath('firstworkingdir', config.firstWorkingDir)
		config.secondWorkingDir = parser['storage'].getpath('secondworkingdir', config.secondWorkingDir)

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

def loadConfig(configfilecontents: str, config: argparse.Namespace = None) -> argparse.Namespace:
	"""Parse the contents of the config (INI) file

	Args:
	  configfilecontents -- The text to parse
	  config (optional) -- An existing argparse.Namespace to be appended to

	Returns:
	  An object of type argparse.Namespace. Access the settings as object attributes (e.g. config.datum).
	"""
	parser = configparser.ConfigParser(converters=CONVERTERS)
	parser.read_string(configfilecontents)
	issues = []

	if not config:
		config = argparse.Namespace()

	__agency_section(parser, config)
	__display_section(parser, config)
	__tabgroups_section(parser, config)
	__reports_section(parser, config)
	__mapping_section(parser, config, issues)
	__storage_section(parser, config)

	for issue in issues:
		LOG.exception(issue)

	return config

__all__ = ("loadConfig")


