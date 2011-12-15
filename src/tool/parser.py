# -*- coding=utf-8 -*-
"""
Should parse kanji frequency html documents
and recreate those as sql/sqlite db.
"""
# std lib
import sys
import urllib

# 3rd party
from BeautifulSoup import BeautifulSoup

# own modules
from db.kanji import Kanji
from db.store import init_db, update_db

def dl_progress(count, blockSize, totalSize):
    percent = int(count * blockSize * 100 / totalSize)
    sys.stdout.write("Download progress: %d%% \r" % percent)

def dl_show_progress(url, file_path):
    file_name = url.split('/')[-1]
    print 'Downloading ' + file_name
    urllib.urlretrieve(url, file_path, reporthook=dl_progress)
    return file_name

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
                    dominance=cols[3].string[:-1])
    update_db()


def create_freq_db(file_path):
    init_db(file_path)
