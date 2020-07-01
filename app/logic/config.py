from dataclasses import dataclass
from app.logic.mapping import Datum, CoordFormat

@dataclass
class Configuration:
	datum: Datum = Datum.WGS84
	coordFormat: CoordFormat = CoordFormat.UTM7

