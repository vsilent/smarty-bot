#!/usr/bin/env python
# -*- coding: utf-8 -*-
import zmq
global sock
from core.config.settings import logger

context = zmq.Context()
sock = context.socket(zmq.REQ)
sock.connect('ipc:///tmp/smarty-scheduler-at')


def add_job(command, hour, minute, sec):
    """ docstring for add_job. """
    global sock

    req = {
        'cmd': 'add_job',
        'command': command,
        'hour': hour,
        'minute': minute,
        'sec': sec
    }
    logger.info('1. Send to scheduler/at.py %s' % req)

    sock.send_json(req, flags=zmq.NOBLOCK)

    return 'job added'

    #c = 0
    #while 1:
        #c = c + 1

        #if c > 100:
            #response = '2. looks like scheduler hanged'
            #break

        #response = sock.recv_json()

        #if response:
            #logger.info('4. response from scheduler/at.py was %s' % response)
            #break

    #return response
    #sock.close()
