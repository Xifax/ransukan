# -*- coding=utf-8 -*-
"""
Prepares all necessary resourses.
"""

import os

from tool.parser import download_freq_html, parse_freq_html, create_freq_db
from pref.opt import paths, links

def do_prepare():
    try:
        # 1.let's download some heavy html lists!
        if not os.path.exists(paths['freq_html']):
            download_freq_html(links['frequency20k'], paths['freq_html'])
        # 2. create/initialize our kanji database
        create_freq_db(paths['freq_db'])
        # 3. let's parse downloaded html and save all the neat stuff to our db
        parse_freq_html(paths['freq_html'])
    # No one knows, what to expect (so lazy)
    except RuntimeError:
        return False
    # GJ!
    return True

if __name__ == "__main__":
    if not do_prepare():
        print 'So sorry! Could not recreate kanji frequency as sqlite db (sadpanda.png)'
