# -*- coding=utf-8 -*-
"""
Aggregator for all the RNG algorithms.
Should be used instead of directly calling submodules lke qrbg and qrng.
"""

from alg.qrbg import qrbg
import numpy as np

from pref.opt import auth
from db.kanji import Kanji

def random_numpy(floating = False):
    return np.random.randint(1, Kanji.query.count())

def random_gsl(floating = False):
    pass

def random_org(floating = False):
    pass

def random_qrBitG(floating = False):
    rand = qrbg(auth['qrbg']['login'], auth['qrbg']['pass'])
    return rand.getShort()

def random_qrNumberG(floating = False):
    pass

algs = {'Quantum Random Number Generator' : random_qrNumberG,
        'Quantum Random Bit Generator'    : random_qrBitG,
        'Random.org'                      : random_org,
        'GNU Scientific Library'          : random_gsl,
        'Numpy random sampling'           : random_numpy,
        }

def random_int(alg = 'Quantum Random Bit Generator'):
    return abs(algs[alg]())

def random_float(alg = 'Quantum Random Bit Generator'):
    return algs[alg](True)

