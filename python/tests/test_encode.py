from os import urandom
from base94 import b94encode
from base94 import py_b94encode
from base94 import rs_b94encode

def test_b94encode_default():
    """
    Test base94 encoding.
    """
    assert b94encode(b'') == b''
    assert b94encode(b'ABC') == b'Wg\\`y'
    assert b94encode(b'123456') == b'Q<-{{@fN'

def test_b94encode_py():
    """
    Test base94 encoding.
    """
    assert py_b94encode(b'') == b''
    assert py_b94encode(b'ABC') == b'Wg\\`y'
    assert py_b94encode(b'123456') == b'Q<-{{@fN'

def test_b94encode_rs():
    """
    Test base94 encoding.
    """
    assert rs_b94encode(b'') == b''
    assert rs_b94encode(b'ABC') == b'Wg\\`y'
    assert rs_b94encode(b'123456') == b'Q<-{{@fN'