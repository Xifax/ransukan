# -*- coding=utf-8 -*-
"""
Prepares all necessary resourses.
"""

import os

from tool.parser import download_freq_html, parse_freq_html, create_freq_db
from pref.opt import links, freqs, db_for_freq

def do_prepare():
    """
    Downloads all required frequency lists, parses those, then recreates as sqlite databases.
    """
    try:
        for freq, freq_path in freqs.items():
            # 1. if none, let's download some heavy html lists!
            if not os.path.exists(freq_path):
                download_freq_html(links[freq], freqs[freq])
            # 2. create/initialize appropriate kanji database
            print "(Re)Initializing database %s " % \
                    db_for_freq[freq]
            create_freq_db(db_for_freq[freq])
            # 3. let's parse downloaded html and save all the neat stuff to our db
            parse_freq_html(freq_path)
        # 4. Selected DB initialization should be performed from UI

    # No one knows, what to expect (so lazy)
    except RuntimeError:
        return False
    # GJ!
    return True

if __name__ == "__main__":
    if not do_prepare():
        print 'So sorry! Could not recreate kanji frequency as sqlite db (sadpanda.png)'
