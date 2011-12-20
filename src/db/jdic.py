# -*- coding=utf-8 -*-
"""
Describes abstractions for kanjidic2.
Note, that jdic2 contains (only) 13K+ unique kanji.
"""

from elixir import Entity, Field, Integer, Unicode, using_options

class KanjiInJDIC(Entity):
    """
    Kanji standard entry in kanjidic2.
    Includes kanji itself, grade, frequency, readings and meaning.
    """

    using_options(tablename="kanji")
    _id = Field(Integer, colname="id", primary_key=True)
    literal = Field(Unicode)
    grade = Field(Integer)
    freq = Field(Integer)
    on_reading = Field(Unicode)
    kun_reading = Field(Unicode)
    meaning = Field(Unicode)

    def __repr__(self):
        return u"Kanji: %s | On: %s | Kun: %s | Meaning: %s" \
        % (self.character, self.on_reading, self.kun_reading, self.meaning)

    @staticmethod
    def search(kanji):
        found = KanjiInJDIC.query().get(kanji)
        if found:
            return found
