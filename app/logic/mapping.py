from enum import Enum, IntEnum
						  
class Datum(Enum):
	WGS84 = 1
	NAD27 = 2  # NAD27 CONUS

	@classmethod
	def possibleValues(cls) -> str:
		return ", ".join([e.name for e in cls])

class CoordFormat(IntEnum):
	UTM7 = 1    # UTM 7x7
	UTM5 = 2    # UTM 5x5
	DEG = 3     # D.d
	DEGMIN = 4  # DM.m
	DMS = 5     # DMS.s

	@classmethod
	def possibleValues(cls) -> str:
		return ", ".join([e.name for e in cls])

	@classmethod
	def displayNames(cls):
		return {cls.UTM7: "UTM 7x7", cls.UTM5: "UTM 5x5", cls.DEG: "D.d°", cls.DEGMIN: "D° M.m'", cls.DMS: "D° M' S.s\""}
	
	def displayName(self) -> str:
		return CoordFormat.displayNames()[self]

