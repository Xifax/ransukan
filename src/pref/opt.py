# -*- coding=utf-8 -*-
"""
Contains some of the widely used project constants and params.
Should be imported only when those are required.
"""

__author__ 	= "Artiom Basenko"
__license__ = "GPL"
__status__ 	= "Development"

# Web resources
links = {'frequency20k' : 'http://foosoft.net/japanese/frequency/downloads/report1.html'}

# Authorization data
		## Quantum Random Number Generator
auth = {'qrng' 	: {'login' 	: 'Xifax',
				   'pass' 	: 'JQWOw735yvEN'},
		## Quantum Random Bit Generator
		'qrbg' 	: {'login' 	: 'Aster',
				   'pass' 	: 'wirel0ss'},
		}

# Relative to main executable: src/ransukan.py
# In case called from tools: should prepend additional ../
paths = {'res' 			: '../res',
		 'lib' 			: '../lib',
		 'freq_html' 	: '../res/frequency20k.html',
		 'freq_db' 		: '../res/freq.db',
		 'kanjidic' 	: '../res/kanjidic2.dblite',
		 }

# Libs to use
libs = { 'qrng' 		: '../lib/libQRNG/libQRNG.so', }
