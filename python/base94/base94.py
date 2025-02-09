# Implementation of Base94 encode and decode in Python 3.
#
# THE GPLv3 LICENSE
# Copyleft (©) 2022 hibays
#

''' 
For example:

>>> from base94 import *

>>> b94encode(b'ABC')
b'Wg\\`y'

>>> b94encode(b'123456')
b'Q<-{{@fN'

>>> b94decode(b'Wg\\`y')
b'ABC'

>>> b94decode(b'Q<-{{@fN')
b'123456'
'''

__all__ = ['b94encode', 'b94decode']

_b94alphabet = (b'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~')
#_b94alphabet = sorted(_b94alphabet)

def b94encode(data,
	## HACK: turn globals into locals
	len=len,
	range=range,
	bnjoin=b''.join,
	from_bytes=int.from_bytes,
	b94tab=[bytes((i,)) for i in _b94alphabet] # The type of (b'ABC')[0] is int. This makes it from int to bytes.
	) -> bytes :
	'''Input bytes-like object, return bytes.
	This algorithm transform 9 bytes to 11 bytes
	The encoded data is about 22.2% larger.
	'''
	b94tab2 = [bnjoin((i, j)) for i in b94tab for j in b94tab] # A simple magic.

	datlen = len(data)
	padding = (-datlen) % 9
	if padding :
		data, datlen = \
			data + b'\0' * padding, datlen + padding
	
	encoded = []
	for i in range(0, datlen, 9) :
		c = from_bytes(data[i: i + 9], 'big') # from data get 9 bytes data to int
		
		# This is faster.
		d2_3 = c // 94
		d4_5 = d2_3 // 8836
		d6_7 = d4_5 // 8836
		d8_9 = d6_7 // 8836

		encoded.append(bnjoin(
			(
				b94tab2[d8_9 // 8836],
				b94tab2[d8_9 % 8836],
				b94tab2[d6_7 % 8836],
				b94tab2[d4_5 % 8836],
				b94tab2[d2_3 % 8836],
				b94tab[c % 94]
			)
		))

	if padding :
		encoded[-1] = encoded[-1][: -padding]

	return bnjoin(encoded)
	
def b94decode(data,
	## HACK: turn globals into locals
	len=len,
	range=range,
	bnjoin = b''.join,
	_intto_byte = int.to_bytes,
	b94nums = {j: i for i,j in enumerate(_b94alphabet)} # dict faster
	) -> bytes :
	'''This function decodes the data that has been encoded by base94.
	Input bytes-like object, return bytes.
	'''
	datlen = len(data)
	padding = (-datlen) % 11
	if padding :
		data, datlen = \
			data + b'~' * padding, datlen + padding
	
	# To revert base94-encoded data. 11 bytes -> 9 bytes.
	# Just like a number of base 94 convert to decimal, each chunk is a number.
	result = bnjoin(
		_intto_byte((((((((((
				 b94nums[data[i    ]] # byte 11
		  * 94 + b94nums[data[i + 1]] # byte 10
		) * 94 + b94nums[data[i + 2]] # byte 9
		) * 94 + b94nums[data[i + 3]] # byte 8
		) * 94 + b94nums[data[i + 4]] # byte 7
		) * 94 + b94nums[data[i + 5]] # byte 6
		) * 94 + b94nums[data[i + 6]] # byte 5
		) * 94 + b94nums[data[i + 7]] # byte 4
		) * 94 + b94nums[data[i + 8]] # byte 3
		) * 94 + b94nums[data[i + 9]] # byte 2
		) * 94 + b94nums[data[i +10]] # byte 1
		, 9, 'big')
		 for i in range(0, datlen, 11)
	)
	
	if padding :
		result = result[: -padding]

	return result

if __name__ == '__main__' :
	from os import system as osSys, name as osName
	osSys('cls' if osName in ('nt', 'dos') else 'clear')

	def c(size, depth=0, pint=('b', 'Kb', 'Mb', 'Gb', 'Tb', 'Pb'))-> str :
		if size > 1024 :
			return c(size/1024, depth+1)
		return '%f%s' % (size, pint[depth])
		
	try :
		from base91 import encode as b91encode, decode as b91decode # type: ignore
	except :
		b91decode = b91encode = lambda _ : str(print('(No Base91 Modular)', end=''))

	from base64 import b64encode, b64decode, b85encode, b85decode
	
	from time import perf_counter
	from os import urandom as osUrandom
	data = osUrandom(1048575)#hash(perf_counter()) & 1048575*16//8)
	
	def _test_mes(base, enData, norData=data) :
		'''A function uses to test the encode and decode function.'''
		t = perf_counter()
		deData = eval('b%ddecode' % base)(enData)
		t = perf_counter() - t
		print('base%d done decoded in %f seconds.' % (base, t))
		if deData == norData :
			return 'Succese! Base%s-encoded data can 100%% revert to normal data.' % (base)
		from difflib import SequenceMatcher as dataSimilarity
		bdesim = dataSimilarity(None, deData, norData).quick_ratio()
		return 'Bad new! Cannot revert %f%% of base%d-encoded data.' % (1e2 - 1e2*bdesim, base)

	def _test_en(base, norData=data) :
		t = perf_counter()
		enTest = eval('b%dencode'%base)(norData)
		t = perf_counter() - t
		print('base%d done encoded in %f seconds.' % (base, t))
		return enTest

	en64,en85,en91,en94 = _test_en(64),_test_en(85),_test_en(91),_test_en(94)
	lno,l64,l85,l91,l94 = len(data), len(en64), len(en85), len(en91), len(en94)
	la = lambda n : 100*n / lno - 100
	
	print()
	#print('normal: %s\nbase64: %s\nbase85: %s\nbase91: %s\nbase94: %s\n'%(data, en64, en85, en91, en94))
	print('normal: %s\nbase64: %d(%.2f%%)\nbase85: %d(%.2f%%)\nbase91: %d(%.2f%%)\nbase94: %d(%.2f%%)\n'%(c(lno), l64, la(l64), l85, la(l85), l91, la(l91), l94, la(l94)))
	print(          '\nbase64: %s\nbase85: %s\nbase91: %s\nbase94: %s\n'%(_test_mes(64, en64), _test_mes(85, en85), _test_mes(91, en91), _test_mes(94, en94)))
