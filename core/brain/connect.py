#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Listen to other services which do not need text reply
"""
from core.config.settings import logger
import zmq


def react(req_obj):

    global brainsock
    context = zmq.Context()
    brainsock = context.socket(zmq.REQ)
    # we will send commands to
    brainsock.connect('ipc:///tmp/smarty-brain')

    """docstring for react"""

    while True:
        if req_obj:
            if not isinstance(req_obj, dict):
                logger.info('react() accepts only dictionary ' +
                            'object like  {"text": "some", "jmsg": "any"} ')
                raise TypeError

            logger.info('brain connector got %s through %s' % (
                req_obj, brainsock
            ))
            brainsock.send_json(req_obj)
            response = brainsock.recv_json()
            req_obj = None
            logger.info('Response from brain connector was : %s' % response)
            return response
