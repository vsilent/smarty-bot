#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Listen to other services which do not need text reply
"""
#import os
from core.config.settings import logger
from core.brain.main import Brain
import zmq


global sock
context = zmq.Context()
sock = context.socket(zmq.REQ)
#we will send commands to
sock.connect('ipc:///tmp/smarty-brain')


def react(req_obj):
    """docstring for react"""
    global sock

    while True:
        if req_obj:
            if not isinstance(req_obj, dict):
                logger.info('react() accepts only dictionary ' +
                            'object like  {"text": "some", "jmsg": "any"} ')
                raise TypeError

            logger.info('brain connector got %s through %s' % (req_obj, sock))
            #logger.info( 'Brain connector has got new request:
            #%s of type %s through %s'  % ( req_obj, type(req_obj), sock)  )
            sock.send_json(req_obj)
            response = sock.recv_json()
            req_obj = None
            logger.info('Response from brain connector was : %s' % response)
            return response
