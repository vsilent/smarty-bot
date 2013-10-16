#!/usr/bin/env python
# -*- coding: utf-8 -*-
from core.config.settings import logger
from broadcast import say, play, bang
import zmq


SERVICE_NAME = 'output'

"""start brain listener, which listens a lot of
publishers except those who need response"""
context = zmq.Context()
sock = context.socket(zmq.SUB)
sock.setsockopt(zmq.SUBSCRIBE, '')

for arg in ['ipc:///tmp/smarty-output']:
    sock.connect(arg)

while True:
    req_obj = sock.recv_json()
    if req_obj:
        logger.info('Output: %s' % req_obj)

        if req_obj['say']:
            bang()
            say(req_obj['say'])

        if req_obj['play']:
            play(req_obj['play'])
