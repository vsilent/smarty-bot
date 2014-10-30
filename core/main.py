#!/usr/bin/env python
# -*- coding: utf-8 -*-

from multiprocessing import Process
from core.config import settings
from core.brain.main import worker
from core.config.settings import logger
import atexit
import zmq
import sys


if settings.JABBER_ENABLED:
    jcontext = zmq.Context()
    jsock = jcontext.socket(zmq.REP)
    jsock.bind('ipc:///tmp/smarty-jabber')

if settings.SPEECH_RECOGNITION_ENABLED:
    jucontext = zmq.Context()
    jusock = jucontext.socket(zmq.REQ)
    jusock.connect('ipc:///tmp/smarty-julius')

#this part is not working yet
# if settings.WEBSOCK_ENABLED:
#     webcontext = zmq.Context()
#     websock = webcontext.socket(zmq.REP)
#     websock.connect('ipc:///tmp/smarty-websocket')

context = zmq.Context()
bsock = context.socket(zmq.REQ)
bsock.connect('ipc:///tmp/smarty-brain')
response = {'text': "error", 'jmsg': 'error', 'type': 'response'}

@atexit.register
def goodbye():
    if settings.SPEECH_RECOGNITION_ENABLED:
        jusock.close()
        jucontext.term()
    if settings.JABBER_ENABLED:
        jsock.close()
        jcontext.term()
    # if settings.WEBSOCK_ENABLED:
    #     websock.close()
    #     webcontext.term()
    bsock.close()
    context.term()

def recursion_on_continue(response, ws, bsock, jsock):
    """
    response - is a response from worker socket
    ws - current worker socket
    bsock - brain socket ( dispatcher who can create new workers )
    jsock - jabber socket ( communicate with client )
    websock - web socket ( communicate with http client )

    """
    # if we have something to do send modified request back to brain
    # check if brain has to create another worker
    req_obj = response.get('req_obj', None)
    error = response.get('error', 0)
    logger.info('recursion started "%s"', response)

    if req_obj:
        # send modified request from worker to brain/main.py again
        logger.info('request a new worker %s', req_obj)
        bsock.send_json(req_obj)
        bresponse = bsock.recv_json()
        wresponse = None

        if isinstance(bresponse, dict):
            w = bresponse.get('worker', None)
            if w:
                # start another worker
                w['addr'] = 'ipc:///tmp/smarty-brain-worker-'
                w['req_obj'] = req_obj
                p = Process(target=worker, kwargs=w)
                p.start()
                w['addr'] = 'ipc:///tmp/smarty-brain-worker-%d' % p.pid
                context = zmq.Context()
                ws = context.socket(zmq.REQ)
                ws.connect(w['addr'])
                ws.send_json({'cmd': 'run'})

                logger.info('Start new worker process to work %s', w['addr'])

                # set timeout
                ws.setsockopt(zmq.LINGER, 0)
                # use poll for timeouts:
                poller = zmq.Poller()
                poller.register(ws, zmq.POLLIN)
                if poller.poll(5*1000):  # 5s timeout in milliseconds
                    wresponse = ws.recv_json()
                else:
                    # raise IOError("Timeout processing worker request")
                    logger.error('Worker %s did not respond in 5 seconds, kill' % w['addr'])
                    # these are not necessary, but still good practice:
                    ws.close()
                    context.term()

                if wresponse:
                    # logger.info('Got response for new worker %s' % wresponse)
                    cont = wresponse.get('continue', None)
                    if cont:
                        logger.info('and recursion again % ', w['addr'])
                        return recursion_on_continue(
                            wresponse, ws, bsock, jsock
                        )

                    logger.info('Worker %s finished job', w['addr'])
                    ws.send_json({'cmd': 'terminate'})
                    ws.close()
                    context.term()
                    return wresponse

        #@todo have to think deeper here
        #do not wait for brain response
        #worker can ask dispatcher( brain ) to put some other worker to work without any response
        #otherwise
        #while 1:
            #if bresponse:
                ##check if new worker has been created
                ##if we can pass dialog to new worker then exit
                #break

    #check if there are messages for jabber
    jmsg = response.get('jmsg', None)
    if jmsg:
        #jabber socket
        jsock.send_json(response)
        while 1:
            jresponse = jsock.recv_json()
            logger.info('Worker returned response %s', jresponse)
            if jresponse:
                #@todo not all arguments passed back to worker,
                #so in the future we need to take care about other args
                #worker remembers previous request
                #ws -current worker socket
                new_request = jresponse
                new_request['cmd'] = 'on_continue'
                new_request['error'] = error
                #@important send to worker previous response from worker itself
                new_request['context'] = response
                logger.info('Worker continues session dialog, \
                            send new request %s to worker', new_request)
                ws.send_json(new_request)

                while 1:
                    response = ws.recv_json()
                    cont = response.get('continue', None)
                    if cont:
                        logger.info('continue second time worked')
                        return recursion_on_continue(
                            response, ws, bsock, jsock)
                    else:
                        return response

while True:

    if settings.SPEECH_RECOGNITION_ENABLED:
        #check activity in julius
        jusock.send_json({"read": 1})
        julius_request = jusock.recv_json()

        if julius_request:
            logger.info('@@@@@ main process has got new request from julius: %s', julius_request)
            #logger.info('<<<<<<<<<< type of message %s' % _obj.get('type', None))
            #send msg to brain listener
            while True:

                bsock.send_json(julius_request)
                response = bsock.recv_json()

                #check workers activity
                workers = response.get('workers', None)
                w = response.get('worker', None)
                if w:
                    w['addr'] = 'ipc:///tmp/smarty-brain-worker-'
                    #logger.info('workers in brain for start %s ' % workers)
                    #logger.info("brain worker %s" % w)
                    p = Process(target=worker, kwargs=w)
                    p.start()
                    #logger.info("..............process %s" % p.pid)
                    w['addr'] = 'ipc:///tmp/smarty-brain-worker-%d' % p.pid
                    logger.info('Run worker %s of type %s', w['addr'], type(w))

                    ws = context.socket(zmq.REQ)
                    ws.connect(w['addr'])
                    ws.send_json({'cmd': 'run'})
                    response = ws.recv_json()
                    cont = response.get('continue', None)
                    #if worker can not complete result and needs
                    #dialog to continue
                    if cont:
                        wresponse = recursion_on_continue(
                            response, ws, bsock, jsock)

                    logger.info('Worker %s finished job', w['addr'])
                    ws.send_json({'cmd': 'terminate'})
                    p.terminate()
                    ws.close()
                    break

                if response:
                    logger.info('last response was: %s', response)
                break

        jusock.send_json({'response': 'ok'})

    if settings.JABBER_ENABLED:
        # check activity in jabber
        jabber_request = jsock.recv_json()
        response = None

        if jabber_request:
            # logger.info('@@@@@@@@@@ main process has got new request from jabber : %s' % jabber_request)
            # logger.info('<<<<<<<<<< type of message %s' % _obj.get('type', None))
            # send msg to brain listener
            bsock.send_json(jabber_request)

            # wait until brain will prepare worker
            # @todo check the type of response
            response = bsock.recv_json()
            if isinstance(response, dict):
                # check workers activity
                workers = response.get('workers', None)
                w = response.get('worker', None)
                if w:
                    w['addr'] = 'ipc:///tmp/smarty-brain-worker-'
                    p = Process(target=worker, kwargs=w)
                    p.start()
                    w['addr'] = 'ipc:///tmp/smarty-brain-worker-%d' % p.pid
                    # logger.info('Run worker %s of type %s' % (w['addr'], type(w)))
                    ws = context.socket(zmq.REQ)
                    ws.connect(w['addr'])
                    ws.send_json({'cmd': 'run'})
                    response = ws.recv_json()

                    if isinstance(response, dict):
                        cont = response.get('continue', None)
                        # if worker can not complete result and needs
                        # to continue dialog then start a recursion
                        # if there are no "request" specified in response
                        # from worker then
                        # we work with the same worker otherwise
                        # a new worker will be created
                        # by worker 'request' in response
                        if cont == 1:
                            logger.info('Worker continues action %s',
                                        w['addr'])
                            response = recursion_on_continue(
                                response, ws, bsock, jsock)
                        else:
                            logger.info('Worker %s finished job', w['addr'])
                            # stop worker's cycle
                            ws.send_json({'cmd': 'terminate'})
                            logger.info('Close worker socket %s', ws)
                            ws.close()
        jsock.send_json(response)

# # this part is not working yet
#     if settings.WEBSOCK_ENABLED:
#         # check activity in web
#         response = None
#         web_request = websock.recv_json()
#
#         if not web_request:
#             websock.send_json(response)
#             continue
#
#         logger.info('Websocket request %s', web_request)
#         continue
#         # send msg to brain listener
#         bsock.send_json(web_request)
#
#         # wait until brain will prepare worker
#         response = bsock.recv_json()
#         if not isinstance(response, dict):
#             websock.send_json(response)
#             continue
#
#         # check workers activity
#         workers = response.get('workers', None)
#         w = response.get('worker', None)
#         if w:
#             w['addr'] = 'ipc:///tmp/smarty-brain-worker-'
#             p = Process(target=worker, kwargs=w)
#             p.start()
#             w['addr'] = 'ipc:///tmp/smarty-brain-worker-%d' % p.pid
#             ws = context.socket(zmq.REQ)
#             ws.connect(w['addr'])
#             ws.send_json({'cmd': 'run'})
#             response = ws.recv_json()
#
#             if isinstance(response, dict):
#                 cont = response.get('continue', None)
#                 # if worker can not complete result and needs
#                 # to continue dialog then start a recursion
#                 # if there are no "request" specified in response
#                 # from worker then
#                 # we work with the same worker otherwise
#                 # a new worker will be created
#                 # by worker 'request' in response
#                 if cont == 1:
#                     logger.info('Worker loops %s', w['addr'])
#                     response = recursion_on_continue(
#                         response, ws, bsock, websock)
#                 else:
#                     logger.info('Worker %s finished job', w['addr'])
#                     # stop worker's loop
#                     ws.send_json({'cmd': 'terminate'})
#                     ws.close()
#
#         websock.send_json(response)

