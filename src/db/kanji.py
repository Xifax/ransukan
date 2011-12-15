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
