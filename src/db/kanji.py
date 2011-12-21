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

    @staticmethod
    def reset_stats():
        """
        Reset selection statistics for every kanji.
        """
        for kanji in Kanji.query.all():
            kanji.picked = 0
        session.commit()

    @staticmethod
    def freq_stats():
        """
        Get picked/frequency distribution.
        """
        return [kanji.picked for kanji in Kanji.query.filter(Kanji.picked > 0).all()],\
                [kanji.frequency for kanji in Kanji.query.filter(Kanji.picked > 0).all()]

    @staticmethod
    def picked_count():
        """
        Get number of kanji picked at least once.
        """
        return Kanji.query.filter(Kanji.picked > 0).count()
