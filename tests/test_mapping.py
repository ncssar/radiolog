import logging

from app.logic.mapping import CoordFormat, CRSCode, Datum, DecimalDegrees

LOG = logging.getLogger("main")


def test_possibleValues():
    assert Datum.possibleValues() == "WGS84, NAD27"
    assert CoordFormat.possibleValues() == "UTM7, UTM5, DEG, DEGMIN, DMS, DEGLIST"


def test_displayName():
    assert CoordFormat.UTM7.displayName() == "UTM 7x7"
    assert CoordFormat.UTM5.displayName() == "UTM 5x5"
    assert CoordFormat.DEG.displayName() == "D.d°"
    assert CoordFormat.DEGMIN.displayName() == "D° M.m'"
    assert CoordFormat.DMS.displayName() == "D° M' S.s\""
    assert CoordFormat.DEGLIST.displayName() == "(Python list)"


def test_fromNMEA():
    def convert(nmea):
        dd = DecimalDegrees.fromNMEA(nmea)
        return (dd.latDd, dd.lonDd)

    # TODO validate that these NMEA conversion tests are correct
    assert convert(["3918.9200", "N", "11955.2100", "W"]) == (39.315333333333335, -119.92016666666666)
    assert convert(["3918.9200", "N", "12055.2100", "W"]) == (39.315333333333335, -120.92016666666666)
    assert convert(["3918.9200", "N", "12155.2100", "W"]) == (39.315333333333335, -121.92016666666666)
    assert convert(["3918.9200", "N", "11959.9900", "W"]) == (39.315333333333335, -119.99983333333333)
    assert convert(["3918.9200", "N", "12000.0000", "W"]) == (39.315333333333335, -120.0)
    assert convert(["3918.9200", "N", "12000.0100", "W"]) == (39.315333333333335, -120.00016666666667)
    assert convert(["3830.0000", "N", "12130.0000", "W"]) == (38.5, -121.5)
    assert convert(["3830.0000", "N", "12115.0000", "W"]) == (38.5, -121.25)
    assert convert(["3830.0000", "N", "12100.0000", "W"]) == (38.5, -121.0)
    assert convert(["3830.0000", "N", "12045.0000", "W"]) == (38.5, -120.75)
    assert convert(["3830.0000", "N", "12030.0000", "W"]) == (38.5, -120.5)
    assert convert(["3830.0000", "N", "12015.0000", "W"]) == (38.5, -120.25)
    assert convert(["3830.0000", "N", "12000.0000", "W"]) == (38.5, -120.0)
    assert convert(["3830.0000", "N", "11945.0000", "W"]) == (38.5, -119.75)
    assert convert(["3830.0000", "N", "11930.0000", "W"]) == (38.5, -119.5)
    assert convert(["3830.0000", "N", "11915.0000", "W"]) == (38.5, -119.25)
    assert convert(["3830.0000", "N", "11900.0000", "W"]) == (38.5, -119.0)
    assert convert(["3845.0000", "N", "12130.0000", "W"]) == (38.75, -121.5)
    assert convert(["3845.0000", "N", "12115.0000", "W"]) == (38.75, -121.25)
    assert convert(["3845.0000", "N", "12100.0000", "W"]) == (38.75, -121.0)
    assert convert(["3845.0000", "N", "12045.0000", "W"]) == (38.75, -120.75)
    assert convert(["3845.0000", "N", "12030.0000", "W"]) == (38.75, -120.5)
    assert convert(["3845.0000", "N", "12015.0000", "W"]) == (38.75, -120.25)
    assert convert(["3845.0000", "N", "12000.0000", "W"]) == (38.75, -120.0)
    assert convert(["3845.0000", "N", "11945.0000", "W"]) == (38.75, -119.75)
    assert convert(["3845.0000", "N", "11930.0000", "W"]) == (38.75, -119.5)
    assert convert(["3845.0000", "N", "11915.0000", "W"]) == (38.75, -119.25)
    assert convert(["3845.0000", "N", "11900.0000", "W"]) == (38.75, -119.0)
    assert convert(["3900.0000", "N", "12130.0000", "W"]) == (39.0, -121.5)
    assert convert(["3900.0000", "N", "12115.0000", "W"]) == (39.0, -121.25)
    assert convert(["3900.0000", "N", "12100.0000", "W"]) == (39.0, -121.0)
    assert convert(["3900.0000", "N", "12045.0000", "W"]) == (39.0, -120.75)
    assert convert(["3900.0000", "N", "12030.0000", "W"]) == (39.0, -120.5)
    assert convert(["3900.0000", "N", "12015.0000", "W"]) == (39.0, -120.25)
    assert convert(["3900.0000", "N", "12000.0000", "W"]) == (39.0, -120.0)
    assert convert(["3900.0000", "N", "11945.0000", "W"]) == (39.0, -119.75)
    assert convert(["3900.0000", "N", "11930.0000", "W"]) == (39.0, -119.5)
    assert convert(["3900.0000", "N", "11915.0000", "W"]) == (39.0, -119.25)
    assert convert(["3900.0000", "N", "11900.0000", "W"]) == (39.0, -119.0)
    assert convert(["3915.0000", "N", "12130.0000", "W"]) == (39.25, -121.5)
    assert convert(["3915.0000", "N", "12115.0000", "W"]) == (39.25, -121.25)
    assert convert(["3915.0000", "N", "12100.0000", "W"]) == (39.25, -121.0)
    assert convert(["3915.0000", "N", "12045.0000", "W"]) == (39.25, -120.75)
    assert convert(["3915.0000", "N", "12030.0000", "W"]) == (39.25, -120.5)
    assert convert(["3915.0000", "N", "12015.0000", "W"]) == (39.25, -120.25)
    assert convert(["3915.0000", "N", "12000.0000", "W"]) == (39.25, -120.0)
    assert convert(["3915.0000", "N", "11945.0000", "W"]) == (39.25, -119.75)
    assert convert(["3915.0000", "N", "11930.0000", "W"]) == (39.25, -119.5)
    assert convert(["3915.0000", "N", "11915.0000", "W"]) == (39.25, -119.25)
    assert convert(["3915.0000", "N", "11900.0000", "W"]) == (39.25, -119.0)
    assert convert(["3930.0000", "N", "12130.0000", "W"]) == (39.5, -121.5)
    assert convert(["3930.0000", "N", "12115.0000", "W"]) == (39.5, -121.25)
    assert convert(["3930.0000", "N", "12100.0000", "W"]) == (39.5, -121.0)
    assert convert(["3930.0000", "N", "12045.0000", "W"]) == (39.5, -120.75)
    assert convert(["3930.0000", "N", "12030.0000", "W"]) == (39.5, -120.5)
    assert convert(["3930.0000", "N", "12015.0000", "W"]) == (39.5, -120.25)
    assert convert(["3930.0000", "N", "12000.0000", "W"]) == (39.5, -120.0)
    assert convert(["3930.0000", "N", "11945.0000", "W"]) == (39.5, -119.75)
    assert convert(["3930.0000", "N", "11930.0000", "W"]) == (39.5, -119.5)
    assert convert(["3930.0000", "N", "11915.0000", "W"]) == (39.5, -119.25)
    assert convert(["3930.0000", "N", "11900.0000", "W"]) == (39.5, -119.0)
    assert convert(["3945.0000", "N", "12130.0000", "W"]) == (39.75, -121.5)
    assert convert(["3945.0000", "N", "12115.0000", "W"]) == (39.75, -121.25)
    assert convert(["3945.0000", "N", "12100.0000", "W"]) == (39.75, -121.0)
    assert convert(["3945.0000", "N", "12045.0000", "W"]) == (39.75, -120.75)
    assert convert(["3945.0000", "N", "12030.0000", "W"]) == (39.75, -120.5)
    assert convert(["3945.0000", "N", "12015.0000", "W"]) == (39.75, -120.25)
    assert convert(["3945.0000", "N", "12000.0000", "W"]) == (39.75, -120.0)
    assert convert(["3945.0000", "N", "11945.0000", "W"]) == (39.75, -119.75)
    assert convert(["3945.0000", "N", "11930.0000", "W"]) == (39.75, -119.5)
    assert convert(["3945.0000", "N", "11915.0000", "W"]) == (39.75, -119.25)
    assert convert(["3945.0000", "N", "11900.0000", "W"]) == (39.75, -119.0)
    assert convert(["4000.0000", "N", "12130.0000", "W"]) == (40.0, -121.5)
    assert convert(["4000.0000", "N", "12115.0000", "W"]) == (40.0, -121.25)
    assert convert(["4000.0000", "N", "12100.0000", "W"]) == (40.0, -121.0)
    assert convert(["4000.0000", "N", "12045.0000", "W"]) == (40.0, -120.75)
    assert convert(["4000.0000", "N", "12030.0000", "W"]) == (40.0, -120.5)
    assert convert(["4000.0000", "N", "12015.0000", "W"]) == (40.0, -120.25)
    assert convert(["4000.0000", "N", "12000.0000", "W"]) == (40.0, -120.0)
    assert convert(["4000.0000", "N", "11945.0000", "W"]) == (40.0, -119.75)
    assert convert(["4000.0000", "N", "11930.0000", "W"]) == (40.0, -119.5)
    assert convert(["4000.0000", "N", "11915.0000", "W"]) == (40.0, -119.25)
    assert convert(["4000.0000", "N", "11900.0000", "W"]) == (40.0, -119.0)


def test_toDEGMIN():
    assert DecimalDegrees(0, 0).toDEGMIN() == (0, 0.0, 0, 0.0)
    assert DecimalDegrees(90, 180).toDEGMIN() == (90, 0.0, 180, 0.0)
    assert DecimalDegrees(38.5, -121.25).toDEGMIN() == (38, 30.0, -121, 15.0)
    assert DecimalDegrees(38.125, -121.025).toDEGMIN() == (38, 7.5, -121, 1.5)


def test_toDMS():
    assert DecimalDegrees(0, 0).toDMS() == (0, 0.0, 0.0, 0, 0.0, 0.0)
    assert DecimalDegrees(90, 180).toDMS() == (90, 0.0, 0.0, 180, 0.0, 0.0)
    assert DecimalDegrees(38.5, -121.25).toDMS() == (38, 30.0, 0.0, -121, 15.0, 0.0)
    assert DecimalDegrees(38.125, -121.025).toDMS() == (38, 7, 30.0, -121, 1, 30.0)


def test_toAlternateFormat():
    dd = DecimalDegrees.fromNMEA(["3830.0000", "N", "12115.0000", "W"])
    assert dd.toAlternateFormat(Datum.WGS84, CoordFormat.UTM5) == "52601  62744"
    assert dd.toAlternateFormat(Datum.WGS84, CoordFormat.UTM7) == "06 52601  42 62744"
    assert dd.toAlternateFormat(Datum.WGS84, CoordFormat.DEG) == "38.500000°N  121.250000°W"
    assert dd.toAlternateFormat(Datum.WGS84, CoordFormat.DEGMIN) == "38° 30.0000'N  121° 15.0000'W"
    assert dd.toAlternateFormat(Datum.WGS84, CoordFormat.DMS) == "38° 30' 0.00\"N  121° 15' 0.00\"W"
    assert dd.toAlternateFormat(Datum.WGS84, CoordFormat.DEGLIST) == [38.5, -121.25]

    # TODO FIXME These do not seem right... for one thing, they are inconsistent betweenm themselves
    assert dd.toAlternateFormat(Datum.NAD27, CoordFormat.UTM5) == "52697  62549"
    assert dd.toAlternateFormat(Datum.NAD27, CoordFormat.UTM7) == "06 52697  42 62549"
    assert dd.toAlternateFormat(Datum.NAD27, CoordFormat.DEG) == "38.500092°N  121.248940°W"
    assert dd.toAlternateFormat(Datum.NAD27, CoordFormat.DEGMIN) == "38° 30.0000'N  121° 14.0000'W"
    assert dd.toAlternateFormat(Datum.NAD27, CoordFormat.DMS) == "38° 30' 0.99\"N  121° 14' 48.56\"W"
    assert dd.toAlternateFormat(Datum.NAD27, CoordFormat.DEGLIST) == [38.50036714, -121.24576155]
