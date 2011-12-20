# -*- coding=utf-8 -*-
"""
Describes abstractions for kanjidic2.
Note, that jdic2 contains (only) 13K+ unique kanji.
"""

from elixir import Entity, Field, Integer, Unicode, \
                    using_options

from pref.opt import paths
from db.store import restore, init_db

class JDIC(Entity):
    """
    Kanji standard entry in kanjidic2.
    Includes kanji itself, grade, frequency, readings and meaning.
    """
    using_options(tablename='kanji')

    _id = Field(Integer, colname='id', primary_key=True)
    literal = Field(Unicode)
    grade = Field(Integer)
    freq = Field(Integer)
    on_reading = Field(Unicode)
    kun_reading = Field(Unicode)
    meaning = Field(Unicode)

    def __repr__(self):
        return u"Kanji: %s | On: %s | Kun: %s | Meaning: %s" \
        % (self.literal, self.on_reading, self.kun_reading, self.meaning)

    def info(self):
        return u"<b>音読み:</b> %s <hr/><b>訓読み:</b> %s <hr/><b>Meaning:</b> %s" \
        % (self.on_reading, self.kun_reading, self.meaning)

    @staticmethod
    def search(kanji):
        init_db(paths['kanjidic'])
        # todo: fix this ugliness
        kanji = unicode(unicode(kanji).encode('utf-8'), 'utf-8')
        found = JDIC.query.filter_by(literal=kanji).first()
        restore()
        return found
