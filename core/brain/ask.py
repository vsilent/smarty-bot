#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Listen to other services which do not need text reply
"""
from core.config.settings import logger
from core.brain.main import Brain
import zmq


SERVICE_NAME = 'get-the-facts'

"""start brain ask machine listener,
which listens to a brain connector socket"""

context = zmq.Context()
sock = context.socket(zmq.REP)
sock.bind('ipc:///tmp/smarty-brain')
empty = {
    'text': 'sorry did not get what you mean',
    'jmsg': "sorry I didn't get", 'type': 'response'
}

while True:
    _obj = sock.recv_json()
    if _obj:

        try:
            request = _obj.get('request', None)
            logger.info("request %s" % request)
            if request:
                request.encode('ascii')
        except UnicodeDecodeError as e:
            logger.info("it was not a ascii-encoded unicode string")
            empty = {
                'text': 'sorry, for now only english is supported, error was %s' % str(e)
                ,'jmsg': "sorry, for now only english is supported, error was %s" % str(e),
                'type': 'response'
            }
            sock.send_json(empty)
            continue
        except UnicodeEncodeError as e:
            logger.info("it was not a ascii-encoded unicode string")
            empty = {
                'text': 'sorry, for now only english is supported, error was %s' % str(e),
                'jmsg': "sorry, for now only english is supported, error was %s" % str(e),
                'type': 'response'
            }
            sock.send_json(empty)
            continue
        else:
            logger.info("It may have been an ascii-encoded unicode string")

        try:
            brain = Brain()
            response = brain.react_on(_obj)
        except Exception as e:
            logger.exception(e)

        if response:
            sock.send_json(response)
        else:
            sock.send_json(empty)
