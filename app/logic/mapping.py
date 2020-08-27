import logging
import math
import re
from enum import Enum, IntEnum
from typing import List

from pyproj import Transformer

LOG = logging.getLogger("main")

NMEACoords = List[str]


class Datum(Enum):
    """Enumeration of the Datum types we can handle."""

    WGS84 = 1
    NAD27 = 2  # same as NAD27 CONUS

    @classmethod
    def possibleValues(cls) -> str:
        return ", ".join([e.name for e in cls])


class CoordFormat(IntEnum):
    """Enumeration of the styles of coordinate formats we can process."""

    UTM7 = 1  # UTM 7x7
    UTM5 = 2  # UTM 5x5
    DEG = 3  # D.d
    DEGMIN = 4  # DM.m
    DMS = 5  # DMS.s
    DEGLIST = 6  # [D.d,D.d] (the only one that's not a string)

    @classmethod
    def possibleValues(cls) -> str:
        return ", ".join([e.name for e in cls])

    @classmethod
    def displayNames(cls):
        return {cls.UTM7: "UTM 7x7", cls.UTM5: "UTM 5x5", cls.DEG: "D.d°", cls.DEGMIN: "D° M.m'", cls.DMS: "D° M' S.s\"", cls.DEGLIST: "(Python list)"}

    def displayName(self) -> str:
        return CoordFormat.displayNames()[self]

    def isUTM(self) -> bool:
        return self in [CoordFormat.UTM5, CoordFormat.UTM7]


class CRSCode(Enum):
    """Enumeration of the Coordinate Reference Systems (CRS) we can process."""

    WGS84_LATLON = 4326  # based on the Earth's center of mass, used by the GPS among others.
    WGS84_UTM = 32600  # (add the UTM zone)
    NAD27_CONUS_LATLON = 4267
    NAD27_CONUS_UTM = 26700  # (add the UTM zone)
    # WEB_MERCATOR = 3857 # e.g. Google Maps and OpenStreetMap

    @classmethod
    def possibleValues(cls) -> str:
        return ", ".join([e.name for e in cls])

    @classmethod
    def perDatumAndFormat(cls, datum: Datum, coordFormat: CoordFormat):
        if datum == Datum.WGS84:
            return CRSCode.WGS84_UTM if coordFormat.isUTM() else CRSCode.WGS84_LATLON
        if datum == Datum.NAD27:
            return CRSCode.NAD27_CONUS_UTM if coordFormat.isUTM() else CRSCode.NAD27_CONUS_LATLON
        raise AttributeError("Unable to determine a CRSCode form the given combination of datum/format.")

    def isUTM(self) -> bool:
        return self in [CRSCode.WGS84_UTM, CRSCode.NAD27_CONUS_UTM]


class DecimalDegrees:
    """
    Our internal representation of a point on the globe, along with various conversion methods.

    Fields:
            datum -- the notation system for these coordinates
            latDd -- the lattitude in degress decimal (negative for south)
            lonDd -- the lattitude in degress decimal (negative for west)
            origDatum, origLatDd, origLonDd -- saved copies of the fields as they were first initialized

    Initialization:
            dd = DecimalDegrees(lat = -118.0, lon = 45.0) # if the decimal degrees are already known
    or
            dd = DecimalDegrees.fromNMEA(nmea = ['3918.9200', 'N', '11955.2100', 'W'])
    or
            #TODO Initializtion method #3: From UTM

    """

    datum: Datum = Datum.WGS84
    latDd: float
    lonDd: float
    origDatum: Datum
    origLatDd: float
    origLonDd: float
    transformer: Transformer
    lastSourceCRS: int = 0
    lastTargetCRS: int = 0

    def __init__(self, lat: float = 0.0, lon: float = 0.0, datum: Datum = Datum.WGS84):
        self.origLatDd = self.latDd = lat
        self.origLonDd = self.lonDd = lon
        self.origDatum = self.datum = datum

    @classmethod
    def validateNMEACoords(cls, nmea: NMEACoords):
        """NMEA coords must be a parsed list of location data from fleetsync in NMEA format"""
        isValid = len(nmea) == 4 and nmea[1] in ["N", "S"] and nmea[3] in ["E", "W"]
        # TODO also validate that nmea[0 and 2] are all digits
        if not isValid:
            raise AttributeError("Invalid NMEA data: {}".format(nmea))

    @classmethod
    def fromNMEA(cls, coords: NMEACoords, datum: Datum = Datum.WGS84):
        "Initialize DecimalDegrees from NMEA coordinates"
        cls.validateNMEACoords(coords)
        latDeg = int(coords[0][0:2])  # first two numbers are degrees
        latMin = float(coords[0][2:])  # remainder is minutes
        lonDeg = int(coords[2][0:3])  # first three numbers are degrees
        lonMin = float(coords[2][3:])  # remainder is minutes
        # add decimal portion of degrees here, before changing sign for hemisphere
        latDd = latDeg + latMin / 60
        lonDd = lonDeg + lonMin / 60
        if coords[1] == "S":
            latDd = -latDd
        if coords[3] == "W":
            lonDd = -lonDd
        return cls(latDd, lonDd, datum)

    def utmZone(self) -> int:
        """The UTM zone (according to the longitude)."""
        return math.floor((self.lonDd + 180) / 6) + 1

    def fromEPSG(self) -> int:
        """Curently, the source CRS is always WGS84_LATLON, since that's what the DecimalDegrees internal storage represents"""
        return CRSCode.WGS84_LATLON.value

    def toEPSG(self, targetDatum, targetFormat) -> int:
        """
        Determine the target EPSG code based on specified datum and format -- and if going to UTM, then also based on
        the UTM zone that corresponds to the original latitude.
        """
        crs: CRSCode = CRSCode.perDatumAndFormat(targetDatum, targetFormat)
        if crs.isUTM():
            return crs.value + self.utmZone()
        return crs.value

    def __estabishTransformer(self, sourceCRS: int, targetCRS: int):
        # Relevant Coordinate Reference Systems (CRS):
        # EPSG:4326 = WGS84 in lat/lon -- based on the Earth's center of mass, used by the GPS among others.
        # EPGS:4267 = NAD27 CONUS (lat/lon)
        # EPGS:32600+zone = WGS84 in UTM (e.g. 32610 = UTM zone 10)
        # EPGS:26700+zone = NAD27 CONUS in UTM (e.g. 26710 = UTM zone 10)
        # FYI:
        # EPSG:3857 = Web Mercator projection used for display by many web-based mapping tools, including Google Maps and OpenStreetMap.
        # EPSG:7789 = International Terrestrial Reference Frame 2014 (ITRF2014), an Earth-fixed system that is independent of continental drift.[4]
        # if target datum is WGS84 and target format is anything other than UTM, just do the math

        # If the source and target CRS's haven't changed, then just re-use the same tranformer from last time
        if sourceCRS != self.lastSourceCRS or targetCRS != self.lastTargetCRS:
            self.lastSourceCRS = sourceCRS
            self.lastTargetCRS = targetCRS
            self.transformer = Transformer.from_crs(sourceCRS, targetCRS)

    def toDEGMIN(self) -> (int, float, int, float):
        """
        Converts decimal degrees to integer degrees and decimal minutes.
        The degrees might be negative.
        The minutes will always be positive.
        """
        latDeg = int(self.latDd)  # might be negative
        latMin = round(float((abs(self.latDd) - float(abs(latDeg))) * 60.0), 8)
        lonDeg = int(self.lonDd)  # might be negative
        lonMin = round(float((abs(self.lonDd) - float(abs(lonDeg))) * 60.0), 8)
        return (latDeg, latMin, lonDeg, lonMin)

    def toDMS(self) -> (int, int, float, int, int, float):
        """
        Converts decimal degrees to a 6-element tuple of integer degrees, integer minutes and decimal seconds for lat and lon.
        The degrees might be negative.
        The minutes and seconds will always be positive.
        """
        (latDeg, latMin, lonDeg, lonMin) = self.toDEGMIN()
        latSec = round(float((latMin - int(latMin)) * 60.0), 8)
        lonSec = round(float((lonMin - int(lonMin)) * 60.0), 8)
        return (latDeg, int(latMin), latSec, lonDeg, int(lonMin), lonSec)

    def toAlternateFormat(self, targetDatum: Datum, targetFormat: CoordFormat):
        """This global position (internally stored as decimal degrees) as converted to the specified format."""
        easting = 0
        northing = 0

        sourceCRS = self.fromEPSG()
        targetCRS = self.toEPSG(targetDatum, targetFormat)
        LOG.debug("Converting from {} to {}".format(sourceCRS, targetCRS))

        if sourceCRS != targetCRS:
            # a transformer is needed for all cases except simple conversions of degree representions (decimals on which part)
            self.__estabishTransformer(sourceCRS, targetCRS)
            t = self.transformer.transform(self.latDd, self.lonDd)
            if targetFormat.isUTM():
                [easting, northing] = map(int, t)
            else:
                # In the case of converting beteen Datums, the lat/lon will be (slightly) different
                [latDd, lonDd] = t
                self.datum = targetDatum
                self.latDd = float(latDd)
                self.lonDd = float(lonDd)

        LOG.debug("Converted from {} {} {} to {} {} {}".format(self.origDatum.name, self.origLatDd, self.origLonDd, self.datum.name, self.latDd, self.lonDd))

        if targetFormat.isUTM():
            eStr = "{0:07d}".format(easting)
            nStr = "{0:07d}".format(northing)
            if targetFormat == CoordFormat.UTM5:
                return "{}  {}".format(eStr[2:], nStr[2:])
            else:
                return "{} {}  {} {}".format(eStr[0:2], eStr[2:], nStr[0:2], nStr[2:])

        # At this point, we are either working with decimal degress as originally stored, or as converted between Datums
        (latDeg, latMin, latSec, lonDeg, lonMin, lonSec) = self.toDMS()
        latLetter = "N" if latDeg >= 0 else "S"
        lonLetter = "E" if lonDeg >= 0 else "W"

        # desired accuracy / digits of precision:
        # at 39 degrees north,
        # 0.00001 degree latitude = 1.11 meters
        # 0.001 minute latutude = 1.85 meters
        # 0.1 second latitude = 3.08 meters
        # (longitude lengths are about 78% as much as latitude, at 39 degrees north)
        if targetFormat == CoordFormat.DEGLIST:
            return [round(self.latDd, 8), round(self.lonDd, 8)]

        if targetFormat == CoordFormat.DEG:
            return "{:.6f}°{}  {:.6f}°{}".format(abs(self.latDd), latLetter, abs(self.lonDd), lonLetter)

        if targetFormat == CoordFormat.DEGMIN:
            return "{}° {:.4f}'{}  {}° {:.4f}'{}".format(abs(latDeg), latMin, latLetter, abs(lonDeg), lonMin, lonLetter)

        if targetFormat == CoordFormat.DMS:
            return "{}° {}' {:.2f}\"{}  {}° {}' {:.2f}\"{}".format(abs(latDeg), int(latMin), latSec, latLetter, abs(lonDeg), int(lonMin), lonSec, lonLetter)

    def __str__(self):
        if (self.datum.name, self.latDd, self.lonDd) == (self.origDatum.name, self.origLatDd, self.origLonDd):
            return "{} {} {}".format(self.datum.name, self.latDd, self.lonDd)
        return "{} {} {} (orig: {} {} {})".format(self.datum.name, self.latDd, self.lonDd, self.origDatum.name, self.origLatDd, self.origLonDd)
