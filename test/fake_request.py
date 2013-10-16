#!/usr/bin/env python
# -*- coding: utf-8 -*-

from core.brain.main import Brain
from core.listen import listen
from core.config.settings import logger
from threading import Timer
from output import say
import sys
from multiprocessing import Process, Queue, Pipe


def testing_jabber():
    """docstring for testing_jabber"""
    from core.brain.jabber_listener import jabber_listener

    this_server, brain_jabber_listener = Pipe()
    jproc = Process( target=jabber_listener, args=( brain_jabber_listener, ) )
    jproc.start()
    msg = {'body':'smarty'}
    this_server.send( msg )
    try:
        response = this_server.recv()
    except EOFError as exc:
        logging.exception( exc )

    print( response )
    jproc.join()

    #prepare fifo

def testing_sound_sensors():
    """docstring for testing_sound_sensors"""
    from core.device.head.sensor.sound.source_direction import read_sensor_data
    q = Queue()
    p = Process(target=read_sensor_data, args=(q,))
    p.start()
    print q.get()
    p.join()


if __name__ == '__main__':

    #test sound source detection
    #try:
        #while 1:
            #testing_sound_sensors()
    #except KeyboardInterrupt:
        #sys.exit(1)

    #path = 'somedir/somedir'
    #import os
    #from config import settings
    #os.makedirs(os.path.join( settings.APP_DIRS['brain_modules_dir'], path ))
    #check reaction
    #b = Brain()
    #brain.react_on('what is your name')
    #import sys
    #if brain.continue_dialog():
        #print 'continue'
    #else:
        #print('stop dialog')
    #sys.exit()
    #testing_jabber()
    #import sys
    #sys.exit(0)
    brain = Brain()

    #brain.react_on('what is broadcasting')
    #brain.react_on('what is kjhdvlkjhasd')
    #brain.react_on('start broadcast')
    #brain.react_on('send email to vs@webdirect.md this is the body text')
    # testing neck motor
    #brain.react_on('turn head to the right')
    #brain.react_on('turn head to the left')
    #brain.react_on('turn head up')
    #brain.react_on('turn head down')
    #brain.react_on('say what time is it now')
    #brain.react_on('update')

    #brain.react_on('show')
    #brain.react_on('play music')

    #brain.react_on('Hi')
    #brain.react_on('what is google')
    #brain.react_on('play music')
    brain.react_on('hi')
    #brain.react_on('say hello')
    #brain.react_on('who are you')
    #import time
    #time.sleep(2)
    #brain.react_on('what time is it')
    #time.sleep(2)
    #brain.react_on('what is your name')
    #time.sleep(2)
    #brain.react_on("tell me please what's your name")
    #time.sleep(2)
    #brain.react_on("your name")
    #time.sleep(2)
    #brain.react_on("name")
    #time.sleep(2)
    #brain.react_on('could you please put the music')
    sys.exit()

    #logging.debug('Start listening...')
    #while(1):
        #listen()
        #request_received = recognize_by_google()
        #if request_received:
            ##react on request
            #brain = Brain()
            ##first request can be greeting with answer in one file
            ##result can be None or the rest part of first request (greeings from beggining cut)
            #rest = brain.react_on(request_received)
            ##in future I need dialog history
            #if not brain.request_processed:
                #start_dialog(rest)
