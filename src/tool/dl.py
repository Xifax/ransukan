# -*- coding=utf-8 -*-
"""
Network/download tools.
"""
import sys
import urllib

def dl_progress(count, blockSize, totalSize):
    percent = int(count * blockSize * 100 / totalSize)
    sys.stdout.write("Download progress: %d%% \r" % percent)

def dl_show_progress(url, file_path=None):
    file_name = url.split('/')[-1]
    print 'Downloading ' + file_name
    if file_path is None:
        file_path = file_name
    urllib.urlretrieve(url, file_path, reporthook=dl_progress)
    return file_name