#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Listen to other services which do not need text reply
"""
import os
from core.config.settings import logger
from core.brain.main import Brain
import zmq
import atexit

SERVICE_NAME = 'brain_listener'

"""start brain listener, which listens to a brain connector socket"""
context = zmq.Context()
sock = context.socket(zmq.REP)
sock.bind( 'ipc:///tmp/smarty-brain' )
empty = {'text': 'no response from smarty', 'jmsg': "sorry I don't know", 'type': 'response'}


@atexit.register
def goodbye():
    sock.close()
    context.term()

while True:
    _obj = sock.recv_json()
    if _obj:
        logger.info( '@@@@@@@@@@ Brain listener has got new request: %s' % _obj )

        try:
            request = _obj.get('request', None)
            logger.info( "request %s" % request )
            if request:
                request.encode('ascii')
        except UnicodeDecodeError as e:
            logger.info( "it was not a ascii-encoded unicode string")
            empty = {'text':'sorry, for now only english is supported, error was %s' % str(e)
                     ,'jmsg':"sorry, for now only english is supported, error was %s" % str(e),
                     'type': 'response'}
            sock.send_json(empty)
            continue
        except UnicodeEncodeError as e:
            logger.info( "it was not a ascii-encoded unicode string")
            empty = {'text':'sorry, for now only english is supported, error was %s' % str(e)
                     ,'jmsg':"sorry, for now only english is supported, error was %s" % str(e),
                     'type': 'response'}
            sock.send_json(empty)
            continue
        else:
            logger.info( "It may have been an ascii-encoded unicode string")


        brain = Brain()
        response = brain.react_on(_obj)
        if response:
            sock.send_json(response)
        else:
            sock.send_json(empty)
