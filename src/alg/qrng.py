# -*- coding=utf-8 -*-

from ctypes import cdll, c_long, pointer

from pref.opt import auth, libs

#lib  = cdll.LoadLibrary("../../lib/libQRNG/libQRNG.so")
#ret = lib.qrng_connect("Xifax", "JQWOw735yvEN")
#if(ret != 0):
	#print "failed to connect!"
#else:
	#print "connected!"

#integer_p = pointer(c_long(0))
#lib.qrng_get_int(integer_p)
#print integer_p.contents

#lib.qrng_disconnect()

class QuantumRNG:

    def __init__(self):
        self.session = False
        self.lib = cdll.LoadLibrary(libs['qrng'])
        if(self.lib.qrng_connect(auth['qrng']['login'],
            auth['qrng']['pass']) == 0):
            self.session = True

    def int(self):
        if(self.session):
            int_p = pointer(c_long(0))
            self.lib.qrng_get_int(int_p)
            return int_p.contents

    def double(self):
        if(self.session):
            return 0.0

    def __del__(self):
        self.lib.qrng_disconnect()

