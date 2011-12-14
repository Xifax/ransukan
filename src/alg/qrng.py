# -*- coding=utf-8 -*-

from ctypes import *

lib  = cdll.LoadLibrary("../../lib/libQRNG/libQRNG.so")
ret = lib.qrng_connect("Xifax", "JQWOw735yvEN")
if(ret != 0):
	print "failed to connect!"
else:
	print "connected!"

integer_p = pointer(c_long(0))
lib.qrng_get_int(integer_p)
print integer_p.contents

lib.qrng_disconnect()
