import configparser
import pathlib
from typing import Optional, List
from dataclasses import dataclass
from enum import Enum

DEFAULT_NAME = 'Search and Rescue'
DEFAULT_LOGO = 'radiolog_logo.jpg'
DEFAULT_CLUE_REPORT = 'clueReportFillable.pdf'
DEFAULT_TIMEOUT = 30

@dataclass
class Configuration:
	agencyName: str = DEFAULT_NAME
	logo: pathlib.Path = pathlib.WindowsPath(DEFAULT_LOGO)
	timeoutMinutes: int = DEFAULT_TIMEOUT # initial timeout interval (valid: 10..120 step 10)
	clueReport: pathlib.Path = pathlib.WindowsPath(DEFAULT_CLUE_REPORT)
	tabGroups: List[str] = None

	def __init__(self):
		self.tabGroups: List[str] = []


