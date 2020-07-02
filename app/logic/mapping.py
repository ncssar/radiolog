import re, math
from enum import Enum, IntEnum
from pyproj import Transformer
from typing import List

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
	DEGLIST = 6 # [D.d,D.d] (the only one that's not a string)

	@classmethod
	def possibleValues(cls) -> str:
		return ", ".join([e.name for e in cls])

	@classmethod
	def displayNames(cls):
		return {cls.UTM7: "UTM 7x7", cls.UTM5: "UTM 5x5", cls.DEG: "D.d°", cls.DEGMIN: "D° M.m'", cls.DMS: "D° M' S.s\""}
	
	def displayName(self) -> str:
		return CoordFormat.displayNames()[self]

	def isUTM(self) -> bool:
		return self in [CoordFormat.UTM5, CoordFormat.UTM7]


class DecimalDegrees():
	"""
	Base representation of a point on the globe. 

	Initializtion method #1:
		dd = DecimalDegrees(-118.0,45.0) # if the decimal degrees are already known

	Initializtion method #2:
		dd = DecimalDegrees()
		dd.fromNMEA(<NMEA>) # where <NMEA> is a list of 4 strings (which will be converted to degrees decimal)

	#TODO Initializtion method #3: From UTM

	"""
	latDd: float
	lonDd: float
	transformer: Transformer
	sourceCRS: int = 0
	targetCRS: int = 0

	def __init__(self, lat: float = 0.0, lon: float = 0.0):
		self.latDd = lat
		self.lonDd = lon

	def fromNMEA(self, coords: List[str]):
		"""coords must be a parsed list of location data from fleetsync in NMEA format"""
		assert len(coords) == 4 
		assert coords[1] in ["N", "S"]
		assert coords[3] in ["E", "W"]

		latDeg = int(coords[0][0:2])  # first two numbers are degrees
		latMin = float(coords[0][2:])  # remainder is minutes
		lonDeg = int(coords[2][0:3])  # first three numbers are degrees
		lonMin = float(coords[2][3:])  # remainder is minutes
		# add decimal portion of degrees here, before changing sign for hemisphere
		self.latDd = latDeg+latMin/60
		self.lonDd = lonDeg+lonMin/60
		if coords[1] == "S":
			self.latDd = -self.latDd
		if coords[3] == "W":
			self.lonDd = -self.lonDd

	def utmZone(self) -> int:
		return  math.floor((self.lonDd+180)/6)+1

	def __estabishTransformer(self, targetDatum: Datum, targetFormat: CoordFormat):
		# relevant CRSes:
		#  4326 = WGS84 lat/lon
		#  4267 = NAD27 CONUS lat/lon
		#  32600+zone = WGS84 UTM (e.g. 32610 = UTM zone 10)
		#  26700+zone = NAD27 CONUS UTM (e.g. 26710 = UTM zone 10)

		# if target datum is WGS84 and target format is anything other than UTM, just do the math

		if targetDatum != Datum.WGS84 or (targetFormat.isUTM()):
			sourceCRS = 4326
			if targetDatum == Datum.WGS84:
				targetCRS = 32600+self.utmZone()
			elif targetDatum == Datum.NAD27:
				if targetFormat.isUTM:
					targetCRS = 26700+self.utmZone()
				else:
					targetCRS = 4267
			else:
				targetCRS = sourceCRS  # fallback to do a pass-thru transformation

			# If the source and target CRS's haven't changed, then just re-use the same tranformer from last time
			if sourceCRS != self.sourceCRS or targetCRS != self.targetCRS:
				self.sourceCRS = sourceCRS
				self.targetCRS = targetCRS
				self.transformer = Transformer.from_crs(sourceCRS, targetCRS)

	def toAlternateFormat(self, targetDatum: Datum, targetFormat: CoordFormat):
		easting = 0
		northing = 0

		self.__estabishTransformer(targetDatum, targetFormat)

		t = self.transformer.transform(self.latDd, self.lonDd)

		if targetFormat.isUTM():
			[easting, northing] = map(int, t)
		else:
			# TODO Are we sure this isn't backwards?
			[lonDd, latDd] = t 
			# Also, why are we bothering to convert from Dd back to Dd? 

		latDd = float(latDd)
		latDeg = int(latDd)
		latMin = float((latDd-float(latDeg))*60.0)
		latSec = float((latMin-int(latMin))*60.0)
		lonDd = float(lonDd)
		lonLetter = "E"
		if lonDd < 0 and targetFormat != CoordFormat.DEGLIST:  # leave it negative for D.dList
			lonDd = -lonDd
			lonLetter = "W"
		lonDeg = int(lonDd)
		lonMin = float((abs(lonDd)-float(abs(lonDeg)))*60.0)
		lonSec = float((abs(lonMin)-int(abs(lonMin)))*60.0)
		# LOG.debug("lonDd="+str(lonDd))
		# LOG.debug("lonDeg="+str(lonDeg))

		# return the requested format
		# desired accuracy / digits of precision:
		# at 39 degrees north,
		# 0.00001 degree latitude = 1.11 meters
		# 0.001 minute latutude = 1.85 meters
		# 0.1 second latitude = 3.08 meters
		# (longitude lengths are about 78% as much as latitude, at 39 degrees north)
		if targetFormat == CoordFormat.DEGLIST:
			return [latDd, lonDd]

		if targetFormat == CoordFormat.DEG:
			return "{:.6f}°N  {:.6f}°{}".format(latDd, lonDd, lonLetter)

		if targetFormat == CoordFormat.DEGMIN:
			return "{}° {:.4f}'N  {}° {:.4f}'{}".format(latDeg, latMin, abs(lonDeg), lonMin, lonLetter)

		if targetFormat == CoordFormat.DMS:
			return "{}° {}' {:.2f}\"N  {}° {}' {:.2f}\"{}".format(latDeg, int(latMin), latSec, abs(lonDeg), int(lonMin), lonSec, lonLetter)

		eStr = "{0:07d}".format(easting)
		nStr = "{0:07d}".format(northing)
		if targetFormat == CoordFormat.UTM7:
			return "{} {}   {} {}".format(eStr[0:2], eStr[2:], nStr[0:2], nStr[2:])

		if targetFormat == CoordFormat.UTM5:
			return "{}  {}".format(eStr[2:], nStr[2:])
