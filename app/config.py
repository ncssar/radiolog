from dataclasses import dataclass
import app.db.config as conf_db
import app.logic.config as conf_logic
import app.ui.config as conf_ui
from app.logic.mapping import Datum, CoordFormat
import utility.config_helpers
import pathlib
import configparser
from app.logic.exceptions import ConfigError

@dataclass
class Configuration:
	db: conf_db.Configuration
	ui: conf_ui.Configuration
	logic: conf_logic.Configuration

def asDatum(input: str) -> Datum:
		return Datum.__members__[input]

def asCoordFormat(input: str) -> CoordFormat:
		return CoordFormat.__members__[input]

CONVERTERS = {
	'path': utility.config_helpers.asPath,
	'datum': asDatum,
	'coordformat': asCoordFormat
}

def loadConfig(configfilecontents: str) -> Configuration:
	parser = configparser.ConfigParser(converters=CONVERTERS)
	parser.read_string(configfilecontents)
	issues = []
	
	config = Configuration(db = conf_db.Configuration(), ui = conf_ui.Configuration(), logic = conf_logic.Configuration())
	
	if parser.has_section('agency'):
		config.ui.agencyName = parser.get(
			'agency', 'name', fallback=config.ui.agencyName)
		config.ui.logo = parser['agency'].getpath('logo', config.ui.logo)

	if parser.has_section('display'):
		config.ui.timeoutMinutes = parser['display'].getint(
			'timeoutminutes', config.ui.timeoutMinutes)

	if parser.has_section('tabgroups'):
		config.ui.tabGroups = []
		for (tabName,tabRE) in parser['tabgroups'].items():
			config.ui.tabGroups.append(tabRE)
	
	if parser.has_section('reports'):
		config.ui.clueReport = parser['reports'].getpath(
			'cluereport', config.ui.clueReport)

	if parser.has_section('mapping'):
		try:
			config.logic.datum = parser['mapping'].getdatum('datum', config.logic.datum)
		except KeyError as e:
			issues.append("The configuration setting of '{0} = {1}' is invalid.".format('datum', e.args[0]))
			issues.append("Possible values are: {0}".format(Datum.possibleValues()))

		try:
			config.logic.coordFormat = parser['mapping'].getcoordformat('coordformat', config.logic.coordFormat)
		except KeyError as e:
			issues.append("The configuration setting of '{0} = {1}' is invalid.".format('coordformat', e.args[0]))
			issues.append("Possible values are: {0}".format(CoordFormat.possibleValues()))


	if parser.has_section('storage'):
		config.db.firstWorkingDir = parser['storage'].getpath(
			'firstworkingdir', config.db.firstWorkingDir)
		config.db.secondWorkingDir = parser['storage'].getpath(
			'secondworkingdir', config.db.secondWorkingDir)

	if issues:
		raise ConfigError("\n".join(issues))

	return config

