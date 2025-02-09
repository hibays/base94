from os import urandom
from base94 import b94encode, b94decode
from base94 import py_b94encode, py_b94decode
from base94 import rs_b94encode, rs_b94decode

def test_cons_ende_default():
    for i in range(1, 512):
        assert b94decode(b94encode(plain:=urandom(i))) == plain

def test_cons_ende_py():
    for i in range(1, 512):
        assert py_b94decode(py_b94encode(plain:=urandom(i))) == plain

def test_cons_ende_rs():
    for i in range(1, 512):
        assert rs_b94decode(rs_b94encode(plain:=urandom(i))) == plain