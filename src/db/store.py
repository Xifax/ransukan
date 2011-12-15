# -*- coding=utf-8 -*-
"""
DB creation and management tools.
"""

import os

from elixir import metadata, create_all, setup_all, session

from pref.opt import paths

def init_db(path = paths['freq_db']):
    metadata.bind = "sqlite:///" + path
    setup_all()
    if not os.path.exists(path):
        create_all()

def update_db():
    session.commit()
