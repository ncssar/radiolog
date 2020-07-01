import configparser
import pathlib
from typing import Optional
from dataclasses import dataclass
from enum import Enum
from typing import Dict

class TabGroups(Dict[str,str]):
	pass

@dataclass
class Configuration:
	agencyName: str = 'SAR'
	logo: pathlib.Path = pathlib.WindowsPath('radiolog_logo.jpg')
	timeoutMinutes: int = 30 # initial timeout interval (valid: 10..120 step 10)
	clueReport: pathlib.Path = pathlib.WindowsPath('clueReportFillable.pdf')
	#tabGroups: TabGroups = {"Numbers": "^Team [A-Z]+"}


