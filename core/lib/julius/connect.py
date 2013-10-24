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

from core.config import settings
from core.config.settings import logger
import sys
import os
import zmq
import pyjulius
import Queue

SERVICE_NAME = 'julius'

#prepare socket for smarty brain listener
context = zmq.Context()
sock = context.socket(zmq.REP)
sock.bind('ipc:///tmp/smarty-julius')

# Initialize and try to connect
client = pyjulius.Client('localhost', 10500)
try:
    client.connect()
except pyjulius.ConnectionError:
    print 'Start julius as module first!'
    sys.exit(1)

# Start listening to the server
client.start()

try:
    while 1:
        #listen to command from main thread
        try:
            result = client.results.get(False)
            if isinstance(result, pyjulius.Sentence):
                logger.info('Julius connector got : %s' % result)
                #print 'Sentence "%s" recognized with score %.2f' % (result, result.score)
                req  = sock.recv_json()
                if req.get('read', None):
                    logger.info('Julius connector got : %s' % req)
                    sock.send_json({'request': str(result), 'from': SERVICE_NAME})
        except Queue.Empty:
            continue
        #print repr(result)
except KeyboardInterrupt:
    print 'Exiting...'
    client.stop()  # send the stop signal
    client.join()  # wait for the thread to die
    client.disconnect()  # disconnect from julius
