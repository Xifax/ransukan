# -*- coding=utf-8 -*-
"""
Aggregator for all the RNG algorithms.
Should be used instead of directly calling submodules lke qrbg and qrng.
"""

from alg.qrbg import qrbg
from alg.qrng import QuantumRNG
import numpy as np

from pref.opt import auth
from db.kanji import Kanji

class MessedUpException(Exception):
    pass

class RandomMess:

    def __init__(self):
        self.qrbg = None
        self.qrng = None
        self.active = next(self.algs.itervalues())

    def auth(self):
        self.qrbg = qrbg(auth['qrbg']['login'], auth['qrbg']['pass'])
        self.qrng = QuantumRNG()

    def set_active(self, alg):
        if alg in self.algs:
            self.active = alg

    def random_short(self):
        pass

    def random_int(self):
        result = self.algs[self.active](self)
        if result is None:
            raise MessedUpException("Could not get random number!")
        return abs(result)

    def random_float(self):
        return abs(self.algs[self.active](self, True))

    # Sub-methods #

    def random_numpy(self, floating = False):
        return np.random.randint(1, Kanji.query.count())

    def random_gsl(self, floating = False):
        pass

    def random_org(self, floating = False):
        pass

    def random_qrBitG(self, floating = False):
        if self.qrbg is None:
            raise MessedUpException("Not authorized on QR-BIT-G service!")
        return self.qrbg.getShort()

    def random_qrNumberG(self, floating = False):
        if self.qrng is None:
            raise MessedUpException("Not authorized on QR-NUMBER-G service!")
        return self.qrng.getInt()

    # Algorithms names and corresponding methods
    algs = {'Quantum Random Number Generator' : random_qrNumberG,
            'Quantum Random Bit Generator'    : random_qrBitG,
            'Random.org'                      : random_org,
            'GNU Scientific Library'          : random_gsl,
            'Numpy random sampling'           : random_numpy,
            }
