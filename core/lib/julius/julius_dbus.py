#! /usr/bin/python -u
# (Note: The -u disables buffering, as else we don't get Julius's output.)
#
# Command and Control Application for Julius
#
# How to use it:
    #  julius -quiet -input mic -C julian.jconf 2>/dev/null | ./command.py
    #
    # Copyright (C) 2008, 2009 Siegfried-Angel Gevatter Pujals <rainct@ubuntu.com>
    #
    # This program is free software: you can redistribute it and/or modify
    # it under the terms of the GNU General Public License as published by
    # the Free Software Foundation, either version 3 of the License, or
    # (at your option) any later version.
    #
    # This program is distributed in the hope that it will be useful,
    # but WITHOUT ANY WARRANTY; without even the implied warranty of
    # MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    # GNU General Public License for more details.
    #
    # You should have received a copy of the GNU General Public License
    # along with this program.  If not, see <http://www.gnu.org/licenses/>.

# Supported commands:
    #
    # This file is provided as an example, and should be modified to suit
    # your needs. As is, it only supports a few commands and executes them on
    # either Rhythmbox or Banshee.

import sys
import os
import gtk
import dbus
import dbus.service
import dbus.glib
import gobject
import logging


class CommandAndControl:

    def run(self, file_object):
        startstring = 'sentence1: <s> '
        endstring = ' </s>'
        line = file_object.readline()
        if not line:
            return
        if 'missing phones' in line.lower():
            logging.debug('Error: Missing phonemes for the used grammar file.')
            sys.exit(1)
        if line.startswith(startstring) and line.strip().endswith(endstring):
            return self.parse(line.strip('\n')[len(startstring):-len(endstring)])


    def parse(self, line):
        params=[param.lower() for param in line.split() if param]
        return ''.join(params).capitalize()


class MyDBUSService(dbus.service.Object):
    def __init__(self):
        bus_name = dbus.service.BusName('com.optibot.julius', bus=dbus.SessionBus())
        dbus.service.Object.__init__(self, bus_name, '/com/optibot/julius')

    @dbus.service.method('com.optibot.julius')
    def listen(self):
        try:
            c = CommandAndControl()
            return c.run(sys.stdin)
        except KeyboardInterrupt:
            sys.exit(1)


myservice = MyDBUSService()
loop = gobject.MainLoop()
loop.run()
