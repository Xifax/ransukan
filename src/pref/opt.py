# -*- coding=utf-8 -*-
"""
Contains some of the widely used project constants and params.
Should be imported only when those are required.
"""

__author__ 	= "Artiom Basenko"
__license__ = "GPL"
__status__ 	= "Development"
__version__ = "0.3"

# Web resources
# todo: add the other
links = {'frequency20k' : 'http://foosoft.net/japanese/frequency/downloads/report1.html',
         'frequency7k'  : 'http://foosoft.net/japanese/frequency/downloads/report10.html',
         # actually, 5.5 ~ from novels
         'frequency5k'  : 'http://foosoft.net/japanese/frequency/downloads/novel/report.html',
         # actually 4.9
         'frequency4k'  : 'http://foosoft.net/japanese/frequency/downloads/report100.html',
        }

# Authorization data
		## Quantum Random ~Number~ Generator
auth = {'qrng' 	: {'login' 	: 'Xifax',
				   'pass' 	: 'JQWOw735yvEN'},
		## Quantum Random ~Bit~ Generator
		'qrbg' 	: {'login' 	: 'Xifax',
				   'pass' 	: 'wirel0ss'},
		}

# Relative to main executable: src/ransukan.py
# In case called from tools: should prepend additional ../
paths = {'res' 			: '../res',
		 'lib' 			: '../lib',
		 'freq_html' 	: '../res/frequency20k.html',
		 'freq_db' 		: '../res/freq.db',
		 'kanjidic' 	: '../res/kanjidic2.dblite',
         'fonts'        : '../res/fonts',
		 }

# Libs to use
libs = {'qrng' 		: '../lib/libQRNG/libQRNG.so',
       }

# Resource names to use for storage
freqs = {'frequency20k' : '../res/frequency20k.html',
         'frequency7k' : '../res/frequency7k.html',
         'frequency5k' : '../res/frequency5k.html',
         'frequency4k' : '../res/frequency4k.html',
        }

# Different databases
dbs = {'Literature compendium, 5.000 Kanji'    : '../res/freq5k.db',
        'JP Wikipedia, 20.000 Kanji'           : '../res/freq20k.db',
        'JP Wikipedia, 7.000 Kanji'            : '../res/freq7k.db',
        'JP Wikipedia, 4.000 Kanji'            : '../res/freq4k.db',
      }

# Correspondence between DBs and frequency charts
db_for_freq = {'frequency20k'  : '../res/freq20k.db',
               'frequency7k'   : '../res/freq7k.db',
               'frequency5k'   : '../res/freq5k.db',
               'frequency4k'   : '../res/freq4k.db',
              }

# Packages to install
packages = ['sqlalchemy', 'elixir', 'BeautifulSoup', 'numpy', 'matplotlib', 'PyQt4']
