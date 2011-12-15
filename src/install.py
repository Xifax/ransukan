# -*- coding=utf-8 -*-
"""
Script to install all necessary libraries and prepare resources.
"""

import sys

try:
    from setuptools.command import easy_install
except ImportError:
    print 'You should install easy_install before using this script...\n'
    if sys.platform == 'win32':
        print 'Windows is badbadbad!'
    else:
        print "In case you're in ubuntu: sudo apt-get install python-setuptools."
    sys.exit(0)

from pref.opt import packages
from prepare import do_prepare

def install_with_easyinstall(package):
    try:
        __import__(package)
        in_system.append(package)
    except ImportError:
        print 'Installing ' + package
        try:
            easy_install.main(['-U', package])
            installed.append(package)
        except RuntimeError:
            problematic.append(package)

def install_info():
    print 'Install/Update complete. Status:\n'
    print '\n'.join(installed), '\n\n(total installed: ' + str(len(installed)) + ')\n'
    print '\n------------ # # # ------------\n'
    print '\n'.join(in_system), '\n\n(already in system: ' + str(len(in_system)) + ')\n'
    print '\n------------ # # # ------------\n'
    print '\n'.join(problematic), '\n\n(erred somehow: ' + str(len(problematic)) + ')\n'
    raw_input('Press any key and so on.')

if __name__ == '__main__':
    installed = in_system = problematic = []
    for pkg in packages:
        install_with_easyinstall(pkg)

    print 'Commencing to download and parse kanji frequency chart. Please, stand by'
    if not do_prepare():
        print 'Sorry! Could not process frequency data.'

    install_info()
