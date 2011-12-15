# -*- coding=utf-8 -*-
"""
Kanji db abstraction.
"""

from elixir import Entity, Field
from elixir import Integer, Float, Unicode

class Kanji(Entity):
    """
    Kanji abstration, frequency distribution.
    """
    rank = Field(Integer)
    character = Field(Unicode)
    frequency = Field(Integer)
    dominance = Field(Float)

    def __repr__(self):
        return u"Kanji: %s | %d" % (self.character, self.frequency)

    @staticmethod
    def get_random(number):
        if number <= Kanji.query.count():
            return Kanji.get(number)
        else:
            return None
