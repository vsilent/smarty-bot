#!/usr/bin/env python
# -*- coding: utf-8 -*-

from core.brain.hello import Reaction

"""
This is just a sample file you can use
for creating a copy/alias of a reaction

1.  Create a directory: mkdir core/brain/good/day/

2.  Copy this file and rename it to reaction.py.
    You will have something like: core/brain/good/morning/reaction.py

3.  Now you will have the functionality of /core/brain/hello/reaction.py
    in your new reaction
4.  Now if you chat to your bot and say
    "good morning" you will get a hello

"""


class ReactionCopy(Reaction):
    def __init__(self, *args, **kwargs):
        """docstring for __init__"""
        super(ReactionCopy, self).__init__()
