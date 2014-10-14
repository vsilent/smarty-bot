#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import logging
from multiprocessing import Process
from os.path import abspath, dirname
sys.path.append(abspath(dirname(abspath(__file__)) + '../../../'))
from core.brain.main import Brain, worker
import zmq
context = zmq.Context()
from optparse import OptionParser

#read request and uuid from command line

opts = {}
parser = OptionParser()

parser.add_option( '-c', '--cmd', action='store', dest='cmd', help = 'command like: ping my sites' )
parser.add_option( '-a', '--arguments', action='store', dest='arguments', help = 'msg arguments: blablabla' )
parser.add_option( '-u', '--uuid', action='store', dest='uuid' , help = 'uuid of an account' )
parser.add_option( '-e', '--email', action='store', dest='email' , help = 'email of an account' )
(opts, args) = parser.parse_args()

if not opts:
    parser.print_help()
request = {'request' : opts.cmd
           ,'from' : 'cron'
           ,'cmd_path' : opts.cmd.split()
           ,'cmd_args' : opts.arguments
           ,'sender' : opts.email
           ,'type' : 'request'
           ,'uuid' : opts.uuid }


b = Brain()
response = b.react_on(request)

logging.info('cron job got a response from brain %s' % response)

##check workers activity
w = response.get('worker', None)

if w:
    w['addr'] = 'ipc:///tmp/smarty-brain-worker-'
    p = Process(target=worker, kwargs=w)
    p.start()
    w['addr'] = 'ipc:///tmp/smarty-brain-worker-%d' % p.pid

    logging.info(
        'Process crontab request, run worker %s of type %s' % (w, type(w))
    )

    ws = context.socket(zmq.REQ)
    ws.connect(w['addr'])
    ws.send_json({'cmd': 'run'})
    response = ws.recv_json()
    if response:
        cont = response.get('continue', None)
        logging.info('continue ? : %s' % cont)
        logging.info('Worker has responded with: %s' % response)
    ws.send_json({'cmd': 'terminate'})
    ws.close()
    p.terminate()
