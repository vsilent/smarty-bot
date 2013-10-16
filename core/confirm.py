#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, os
app_dir =  os.path.normpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
sys.path.append(os.path.dirname(app_dir))
sys.path.append(os.path.dirname(app_dir) + '/../')

from core.lib.db.adapter import Database

class Confirm:
    """class Confirm"""
    db = ''
    record = ''
    state = False

    def __str__(self):
        return  __name__

    def __init__(self, sentense):
        self.db = Database()
        if len(sentense) != 0 :
            self.record = self.get_one_by('sentense', sentense)
            if self.record is None:
                self.ask(sentense)

    def get_record(self):
        return self.record

    def ask(self, sentense):
        self.db.cursor.execute("insert into confirm (sentense, state) values (?, ?)", ( sentense, False ) )
        self.db.connection.commit()

    def confirm(self, state):
        """docstring for set_state"""
        if self.record:
            self.db.cursor.execute("update confirm SET state = ? WHERE sentense= ?", ( state, self.record[1] ) )
            self.db.connection.commit()

    def get_one_by(self, key, value):
        self.db.cursor.execute( "SELECT * FROM confirm WHERE sentense = ?",  ( value, ) )
        rs =  self.db.cursor.fetchall()
        if rs:
            return rs[0]

    def get_state(self, sentence):
        if self.record is not None:
            return self.record[2]


    def del_record(self):
        if self.record is not None:
            #print(type(self.record[1]))
            print("removing %s" % self.record[1])
            self.db.cursor.execute("DELETE FROM `confirm` WHERE LOWER(sentense) = LOWER(?) ", (self.record[1],) )
            self.db.connection.commit()
