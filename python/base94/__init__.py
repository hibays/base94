__all__ = ['b94encode', 'b94decode', 'rs_b94encode', 'rs_b94decode', 'py_b94encode', 'py_b94decode']

from .base94 import b94encode as py_b94encode, b94decode as py_b94decode

try :
	from ._base94 import b94encode, b94decode
	rs_b94encode, rs_b94decode = b94encode, b94decode
except ImportError :
	rs_b94encode, rs_b94decode = None, None

b94encode = py_b94encode if rs_b94encode is None else rs_b94encode

b94decode = py_b94decode if rs_b94decode is None else rs_b94decode
