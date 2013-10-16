#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Control robot's neck stepper motor 1
    default port 888 (378h)
    One motor turnover takes 200 steps
"""
import parallel
import logging
import signal
import sys
import time
DELAY = 0.01
import multiprocessing


class TimeoutException(Exception):
    pass



class SoundSensor1():

    def __init__( self ):
        """docstring for __init__"""
        self.port = parallel.Parallel()

    def listen( self ):
        """docstring for step_clockwise"""
        i11 = self.port.getInBusy()
        i12 = self.port.getInPaperOut()
        if ( i11 == False or i12 == False ):
            #print( 'pin 11 : %s  pin 12: %s' % ( i11, i12 ) )
            direction = self.calculate()
            #if direction:
                #print "left"
            #else:
                #print "right"

            return direction

    def calculate( self ):
        def timeout_handler( signum, frame ):
            raise TimeoutException()

        signal.signal(signal.SIGALRM, timeout_handler)
        signal.alarm(1) # triger alarm in 1 seconds

        si11 = 0
        si12 = 0
        try:
            while( 1 ):
                if self.port.getInBusy() == False:
                    si11 = si11 + 1

                if self.port.getInPaperOut() == False:
                    si12 = si12 + 1

        except TimeoutException:
            print( 'pin 11: %s' % si11)
            res = ( si11 > si12 )
            print( 'pin 12: %s' % si12)
            si11 = 0
            si12 = 0
            return res


def read_sensor_data(queue):
    """docstring for read_sensor_data"""
    s = SoundSensor1()
    p = multiprocessing.current_process()
    logging.info("Starting %s %d" % ( p.name, p.pid ))
    sys.stdout.flush()
    data = s.listen()
    queue.put([data])


#if __name__ == '__main__':
    #try:
        #s = SoundSensor1()
        #while 1:
            #s.listen()
    #except KeyboardInterrupt:
        #sys.exit(1)

#def process_request(self, msg):

    ##set 20 sec timeout for the child process
    ##timeout = 20
    ##logging.info('Set process timeout 20 sec')
    #self.this_server, brain_jabber_listener = Pipe()
    #self.jproc = Process( target=jabber_listener, args=( brain_jabber_listener, ) )
    #self.jproc.start()
    #logging.info( "received:  %s  from %s " , msg['body'], msg['from'] )

    #"""docstring for process_request"""
    #self.this_server.send( [ msg['body'] ] )
    #try:
        #self.jresponse = self.this_server.recv()
    #except EOFError as exc:
        #logging.exception( exc )
    #self.jproc.join()

##multiprocessing method
#def sound_source_direction_listener(conn):
    #"""/device/head/sensor/sound/source_direction.py listener"""
    #request = None
    #while request is None:
        #try:
            ##get list object
            #request = conn.recv()
            ##join all list items into one string
            #request = ' '.join(request)
        #except EOFError as exc:
            #logging.exception(exc)

        #if request is not None:
            #logging.info("request from jabber at brain.jabber_listener %s " , (request,))

            #brain = Brain()
            #try:
                #brain.react_on(request)
                #if brain._request_processed:
                    #if brain._response is not None:
                        #response = brain._response
                    #else:
                        #response = 'Your request processed successfully'
                #else:
                    #response = 'Robot did not return any response'
            #except RuntimeError as exception:
                #response = 'unknown command'
                #logging.exception(exception)

            #conn.send( [ response ] )
            #conn.close()

##import os
##import logging
##import sys
###import tempfile

##tmpdir = '/tmp'
##filename = os.path.join(tmpdir, 'device_head_sensor_sound_source_direction_fifo')

##if os.path.isfile(filename):
    ##try:
        ##os.remove(filename)
    ##except OSError as e:
        ##pass

##try:
    ##os.mkfifo(filename)
##except OSError as e:
    ##logging.exception(e)
    ##logging.exception("Clean up..")
    ##os.remove(filename)

##while(1):
    ##response = sys.stdin.readline()
    ##if response is not None:
        ##fifo = open(filename, 'w')
        ##fifo.write( response )
        ##fifo.close()
