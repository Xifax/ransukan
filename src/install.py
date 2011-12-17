# -*- coding=utf-8 -*-
"""
Script to install all necessary libraries and prepare resources.
"""
import os
import subprocess
import sys

from tool.dl import dl_show_progress

def download_and_install(file_url):
    file = dl_show_progress(file_url)
    subprocess.call('./' + file)
    os.remove('./' + file)

try:
    from setuptools.command import easy_install
except ImportError:
    print 'You should install easy_install before using this script...\n'
    if sys.platform == 'win32':
        print 'Windows is very no-no, reconsider at once!\n'
        if raw_input('Well, if you DO insist... Download setuptools now? [y/n]: ') == ('y' or 'Y'):
            download_and_install('http://pypi.python.org/packages/2.7/s/setuptools/setuptools-0.6c11.win32-py2.7.exe#md5=57e1e64f6b7c7f1d2eddfc9746bbaf20')
            print "\nOK. Now, please, re-run install script. Thank you. (I'm trying to be polite, you see)."
    else:
        print "You're running unix-based os (no, really)! In case you're in ubuntu: sudo apt-get install python-setuptools."
    sys.exit(0)

from pref.opt import packages

def install_with_easyinstall(package):
    try:
        __import__(package)
        in_system.append(package)
    except ImportError:
        print 'Installing ' + package + '...'
        try:
            easy_install.main(['-U', package])
            installed.append(package)
        except Exception:
            problematic.append(package)

def install_info():
    print 'Installation complete.\n\nInstalled: %s, (total: %d) \
    \n\nIn system: %s, (total: %d)  \n\nErred: %s, (total: %d)' \
    % ('\n'.join(installed), len(installed),
        '\n'.join(in_system), len(in_system),
        '\n'.join(problematic), len(problematic))
    raw_input('Press any key and so on.')

def intro():
    if not raw_input('Good day! This script will now commence to install all the required python libs, \
download and prepare necessary resources and so on.\n\
In case something goes terribly wrong (e.g., setuptools breaks on some nonexistent script or tries to install incompatible windows lib) - you may manually install packages (specified in README) \
then run prepare.py.\n\nWell, shall we begin now? [y/n]: ') == ('y' or 'Y'):
        print "\nOh, it's a pity then. So long and thanks for the shell."
        sys.exit(0)
    print '\nA wise choice!\n'

if __name__ == '__main__':
    intro()

    installed, in_system, problematic = [], [], []
    for pkg in packages:
        install_with_easyinstall(pkg)

    from prepare import do_prepare
    print 'Commencing to download and parse kanji frequency charts.\nShould parse quite large HTML files, so it may take quite some time. Please, stand by...\n'
    if not do_prepare():
        print '\nSorry! Could not process frequency data.'

    install_info()
