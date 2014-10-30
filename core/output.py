#!/usr/bin/env python
# -*- coding: utf-8 -*-
from core.config.settings import logger
from broadcast import say, play, bang
import zmq
import atexit

SERVICE_NAME = 'output'

"""subscribe for a smarty output
no need response"""
out_context = zmq.Context()
outsock = out_context.socket(zmq.SUB)
outsock.setsockopt(zmq.SUBSCRIBE, '')

for arg in ['ipc:///tmp/smarty-output']:
    outsock.connect(arg)

@atexit.register
def goodbye():
    outsock.close()
    out_context.term()

while True:
    req_obj = outsock.recv_json()
    if req_obj:
        logger.info('Output: %s' % req_obj)

        if req_obj['say']:
            bang()
            say(req_obj['say'])

        if req_obj['play']:
            play(req_obj['play'])

        if req_obj['jmsg']:
            pass
