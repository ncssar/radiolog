from app.logic.mapping import Datum, CoordFormat

def test_possibleValues():
    assert Datum.possibleValues() == "WGS84, NAD27"
    assert CoordFormat.possibleValues() == "UTM7, UTM5, DEG, DEGMIN, DMS"

def test_displayName():
    assert CoordFormat.UTM7.displayName() == "UTM 7x7"
    assert CoordFormat.UTM5.displayName() == "UTM 5x5"
    assert CoordFormat.DEG.displayName() == "D.d°"
    assert CoordFormat.DEGMIN.displayName() == "D° M.m'"
    assert CoordFormat.DMS.displayName() == "D° M' S.s\""
