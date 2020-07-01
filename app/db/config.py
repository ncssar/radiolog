import pathlib
from typing import Optional
from dataclasses import dataclass

@dataclass
class Configuration:
	firstWorkingDir: pathlib.Path = pathlib.WindowsPath('testdata')
	secondWorkingDir: Optional[pathlib.Path] = None
