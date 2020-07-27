import app.config
from app.logic.mapping import Datum, CoordFormat
from pathlib import WindowsPath
from app.logic.exceptions import  RadioLogConfigError
from typing import List

def test_config_all_defaults():
    config = app.config.loadConfig("")

    assert config.ui.agencyName == 'Search and Rescue'
    assert config.ui.logo == WindowsPath('radiolog_logo.jpg')
    assert config.ui.timeoutMinutes == 30
    assert len(config.ui.tabGroups) == 0
    assert config.ui.clueReport == WindowsPath('clueReportFillable.pdf')
    assert config.logic.datum == Datum.WGS84
    assert config.logic.coordFormat == CoordFormat.UTM7
    assert config.db.firstWorkingDir == WindowsPath('testdata')
    assert config.db.secondWorkingDir == None

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
    config = app.config.loadConfig(ini)

    assert config.ui.agencyName == 'International Rescue'
    assert config.ui.logo == WindowsPath('thunderbirds.png')
    assert config.ui.timeoutMinutes == 20
    assert len(config.ui.tabGroups) == 1
    assert config.ui.tabGroups[0] == "^Thunderbird [A-Z]+"
    assert config.ui.clueReport == WindowsPath('fabclue.pdf')
    assert config.logic.datum == Datum.NAD27
    assert config.logic.coordFormat == CoordFormat.DMS
    assert config.db.firstWorkingDir == WindowsPath('C:\\ir')
    assert config.db.secondWorkingDir == WindowsPath('E:\\fab')
    # TODO (more tests?)


def test_config_bad():
    ini = """
[mapping]
datum = XXX
coordformat = XXX
    """
    try:
        config = app.config.loadConfig(ini)
    except  RadioLogConfigError as e:
        assert e.message == """The configuration setting of 'datum = XXX' is invalid.
Possible values are: WGS84, NAD27
The configuration setting of 'coordformat = XXX' is invalid.
Possible values are: UTM7, UTM5, DEG, DEGMIN, DMS, DEGLIST"""

