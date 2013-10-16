#!/usr/bin/env python
# -*- coding: utf-8 -*-

from core.brain.goodbye.reaction import Reaction


class ReactionCopy(Reaction):
    def __init__(self, *args, **kwargs):
        """docstring for __init__"""
        super(ReactionCopy, self).__init__()
