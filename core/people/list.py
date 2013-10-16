
#!/usr/bin/env python
# -*- coding: utf-8 -*-

from core.lib.db.mongo import Mongo

class List():
    """class Person"""

    def __init__(self, filter=None):
        self.filter = filter
        self.mongo = Mongo()
        self.mongo.connect()
        self.collection = self.mongo.db.person

    def __str__(self):
        return  __name__

    def find(self):
        """docstring for find"""
        return self.collection.find(self.filter)
