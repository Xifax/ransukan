# -*- coding=utf-8 -*-
"""
Kanji db abstraction.
"""

from elixir import Entity, Field, Integer, Float, Unicode, session

class Kanji(Entity):
    """
    Kanji abstration, based on frequency distribution.
    Also includes dominance and statistics fields.
    """

    rank = Field(Integer)
    character = Field(Unicode)
    frequency = Field(Integer)
    dominance = Field(Float)
    picked = Field(Integer)

    def __repr__(self):
        return u"Kanji: %s | %d" % (self.character, self.frequency)

    @staticmethod
    def get_random(number):
        """
        Get random kanji and increment it's stats.
        If provided number exceeds available kanji rank: will return None.
        """
        if number <= Kanji.query.count():
            kanji = Kanji.get(number)
            kanji.picked += 1
            session.commit()
            return kanji
            #return Kanji.get(number)
        else:
            return None

    @staticmethod
    def reset_stats():
        """
        Reset selection statistics for every kanji.
        """
        for kanji in Kanji.query.all():
            kanji.picked = 0
        session.commit()

