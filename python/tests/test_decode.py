from os import urandom
from base94 import b94decode
from base94 import py_b94decode
from base94 import rs_b94decode

def test_b94decode_default():
    """
    Test base94 encoding.
    """
    assert b94decode(b'') == b''
    assert b94decode(b'Wg\\`y') == b'ABC'
    assert b94decode(b'Q<-{{@fN') == b'123456'

def test_b94decode_py():
    """
    Test base94 encoding.
    """
    assert py_b94decode(b'') == b''
    assert py_b94decode(b'Wg\\`y') == b'ABC'
    assert py_b94decode(b'Q<-{{@fN') == b'123456'

def test_b94decode_rs():
    """
    Test base94 encoding.
    """
    assert rs_b94decode(b'') == b''
    assert rs_b94decode(b'Wg\\`y') == b'ABC'
    assert rs_b94decode(b'Q<-{{@fN') == b'123456'