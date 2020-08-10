import time
from app.logic.entries import rreplace

def test_rreplace():
    assert rreplace("foobarbar","bar","",1) == "foobar"
    assert rreplace("foobarbar","bar","",9) == "foo"
    assert rreplace("barbarfoobarbar","bar","",3) == "barfoo"
    # TODO (more tests)
