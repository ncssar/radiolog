import time
from utility.misc_functions import *

def test_timestamp():
    currentTime = time.strptime("30 Jun 20 13:59:59", "%d %b %y %H:%M:%S")
    assert timestamp(currentTime) == "2020_06_30_135959"
    # TODO (more tests?)

def test_normName():
    assert normName("Plain123") == "Plain123"
    assert normName("Percent%Sign") == "Percent_Sign"
    assert normName(" Leading and Middle Spaces") == "_Leading_and_Middle_Spaces"
    # TODO (more tests)

def test_rreplace():
    assert rreplace("foobarbar","bar","",1) == "foobar"
    assert rreplace("foobarbar","bar","",9) == "foo"
    assert rreplace("barbarfoobarbar","bar","",3) == "barfoo"
    # TODO (more tests)
