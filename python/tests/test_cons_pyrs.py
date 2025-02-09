from os import urandom
from base94 import py_b94encode, py_b94decode
from base94 import rs_b94encode, rs_b94decode

def test_cons_encode_pyrs():
    """
    Test base94 encoding.
    """
    for i in range(1, 512):
        assert py_b94encode(plain:=urandom(i)) == rs_b94encode(plain)
        
def test_cons_decode_pyrs():
    """
    Test base94 decoding.
    """
    for i in range(1, 512):
        print(rs_b94encode(urandom(i)))
        assert py_b94decode(ub94d := py_b94encode(urandom(i))) == rs_b94decode(ub94d)
        assert py_b94decode(ub94d := rs_b94encode(urandom(i))) == rs_b94decode(ub94d)