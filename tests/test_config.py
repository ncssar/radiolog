import logging
import sys
from gwpycore import setup_logging
from app.config import load_config
from app.logic.mapping import Datum, CoordFormat
from pathlib import Path
from app.logic.exceptions import  RadioLogConfigError
from typing import List

def test_config_all_defaults():
	setup_logging.cache_clear()
	log = setup_logging("main", logfile=None, nocolor=True)
	config = load_config(ini="")

	assert config.agencyName == 'Search and Rescue'
	assert config.logo == Path('radiolog_logo.jpg')
	assert config.timeoutMinutes == 30
	assert len(config.tabGroups) == 0
	assert config.clueReport == Path('clueReportFillable.pdf')
	assert config.datum == Datum.WGS84
	assert config.coordFormat == CoordFormat.UTM7
	assert config.firstWorkingDir == Path('testdata')
	assert config.secondWorkingDir == None

def test_config_all_good():
	ini = """
[agency]
name = International Rescue
logo = thunderbirds.png

[mapping]
datum = NAD27
coordformat = DMS

[display]
timeoutminutes = 20

[tabgroups]
Numbers = ^Thunderbird [A-Z]+

[reports]
cluereport = fabclue.pdf

[storage]
firstworkingdir = C:\\ir
secondworkingdir = E:\\fab
	"""
	setup_logging.cache_clear()
	log = setup_logging("main", logfile=None, nocolor=True)
	config = load_config(ini=ini)

	assert config.agencyName == 'International Rescue'
	assert config.logo == Path('thunderbirds.png')
	assert config.timeoutMinutes == 20
	assert len(config.tabGroups) == 1
	assert config.tabGroups[0] == "^Thunderbird [A-Z]+"
	assert config.clueReport == Path('fabclue.pdf')
	assert config.datum == Datum.NAD27
	assert config.coordFormat == CoordFormat.DMS
	assert config.firstWorkingDir == Path('C:\\ir')
	assert config.secondWorkingDir == Path('E:\\fab')
	# TODO (more tests?)


def test_config_bad(capsys):
	ini = """
[mapping]
datum = XXX
coordformat = XXX
	"""
	sys.stderr.write("==START==\n")
	setup_logging.cache_clear()
	log = setup_logging("main", logfile=None, nocolor=True)
	config = load_config(ini=ini)
	sys.stderr.write("==END==")
	captured = capsys.readouterr()
	assert captured.out == ""
	assert captured.err == """==START==
WARNING The configuration setting of [mapping]datum = XXX is invalid. Possible values are: WGS84, NAD27
WARNING The configuration setting of [mapping]coordformat = XXX is invalid. Possible values are: UTM7, UTM5, DEG, DEGMIN, DMS, DEGLIST
==END=="""


