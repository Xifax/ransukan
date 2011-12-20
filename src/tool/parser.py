# -*- coding=utf-8 -*-
"""
Should parse kanji frequency html documents
and recreate those as sql/sqlite db.
"""

# 3rd party
from BeautifulSoup import BeautifulSoup

# own modules
from db.kanji import Kanji
from db.store import init_db, update_db
from tool.dl import dl_show_progress

def download_freq_html(url, file_path):
    dl_show_progress(url, file_path)

def parse_freq_html(file_path):
    with file(file_path) as f:
        html = f.read()
        f.close()
    soup = BeautifulSoup(html)
    kanji_table = soup.find('table')
    for row in kanji_table.findAll('tr'):
        cols = row.findAll('td')
        if cols:
            Kanji(  rank=cols[0].string,
                    character=cols[1].a.string,
                    frequency=cols[2].string,
                    dominance=cols[3].string[:-1],
                    picked=0)
    update_db()

def create_freq_db(file_path):
    """
    Create or initialize specified DB file.
    """
    init_db(file_path)
