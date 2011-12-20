# -*- coding=utf-8 -*-
"""
DB creation and management tools.
"""

import os

from elixir import metadata, create_all, setup_all, session

from pref.opt import paths, dbs

# Currently mapped db (name)
active_db = next(dbs.iterkeys())

class NoDbException(Exception):
    pass

def init_db(path = paths['freq_db']):
    """
    Initialize specified DB.
    In case no DB file exists, it will be created.
    """
    metadata.bind = "sqlite:///" + path
    setup_all()
    if not os.path.exists(path):
        create_all()

def update_db():
    """
    Commit updated data to currently mapped DB.
    """
    session.commit()

def choose_db(db):
    """
    Remap active DB.
    """
    global active_db
    if os.path.exists(dbs[db]):
        metadata.bind = "sqlite:///" + dbs[db]
        setup_all()
        active_db = db
    else:
        raise NoDbException("Specified db does not exist!")

def restore():
    """
    Remap previously active db.
    """
    init_db(dbs[active_db])
