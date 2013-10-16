#!/usr/bin/env python
# -*- coding: utf-8 -*-

#import multiprocessing
#from multiprocessing import Process, Queue
#import os
#import sys
#import dbus
#import tempfile
#from core.device.head.sensor.sound.source_direction import read_sensor_data
#from core.main import main
import sys
import os
from core.config import settings
from core.config.settings import logger
import subprocess
import signal

app_dir = os.path.normpath(os.path.join(os.getcwd(),
                                        os.path.dirname(__file__)))
sys.path.append(os.path.dirname(app_dir))
sys.path.append(os.path.dirname(app_dir) + '/../')


def process_exists(process):
    """docstring for process_exists"""
    #import commands
    #output = commands.getoutput('pidof %s |wc -w' % process)
    pid = False
    g = os.popen("ps -e -o pid,command")
    for line in g.readlines():
        if process in line:
            pid = line.strip().split(' ')[0]
            break
    return pid


if __name__ == '__main__':
    jobs = []

    try:

        #start brain listener at socket
        #start main process
        #p = Process(target=Brain.listen())
        #jobs.append(p)
        #p.daemon = True
        #p.start()
        #julius_proc.communicate()
        #logger.debug(julius_proc.communicate()[0])

        if settings.JABBER_ENABLED:
            #start jabber
            jpid = process_exists('jabber/connect.py')
            if not jpid:
                logger.info('Start jabber connector subprocess '
                            + "%s/core/lib/jabber/connect.py"
                            % settings.ROBOT_DIR)
                jabber_proc = subprocess.Popen(
                    ["python", "%s/core/lib/jabber/connect.py"
                     % settings.ROBOT_DIR]
                )
                #jabber_proc.communicate()
                #logger.info("process id: %s", jabber_proc.communicate())
            else:
                logger.info('Jabber connector is already running, skip...')

            jmpid = process_exists('jabber/mucbot.py')

            if not jmpid:
                logger.info('Start jabber multi user chat bot subprocess '
                            + "%s/core/lib/jabber/mucbot.py"
                            % settings.ROBOT_DIR)
                mjabber_proc = subprocess.Popen(
                    ["python", "%s/core/lib/jabber/mucbot.py"
                     % settings.ROBOT_DIR]
                )
                #jabber_proc.communicate()
                #logger.info("process id: %s", jabber_proc.communicate())
            else:
                logger.info('Jabber multiuser chat bot is already running, skip...')
        ## start sensor fifo output process
        #sensor1_proc = subprocess.Popen(
            #["python" ,
            #"%s/core/device/head/sensor/sound/source_direction.py"
            #% settings.ROBOT_DIR],
            #shell=False,
            #stdin=subprocess.PIPE,
            #stdout=subprocess.PIPE )

        #logger.info("%s", sensor1_proc.communicate())

        #q = Queue()
        #p = Process(target=read_sensor_data, args=(q,))
        #p.start()
        #jobs.append(p)

        #join proceses
        #for p in jobs:
            ##direction = q.get()
            #p.join()

            #logger.info("%s", julius_proc.communicate())
        #else:
            #logger.info('Julius is already running, skip...')
        opid = process_exists('core/output.py')
        if not opid:
            logger.info("Start output subprocess")
            brain_proc = subprocess.Popen(
                ["python", "%s/core/output.py" % settings.ROBOT_DIR]
            )
        else:
            logger.info("Output process already running, skip...")

        bpid = process_exists('brain/listener.py')
        if not bpid:
            logger.info("Start brain listener subprocess")
            brain_proc = subprocess.Popen(
                ["python", "%s/core/brain/listener.py" % settings.ROBOT_DIR]
            )
        else:
            logger.info("Brain listener subprocess already running, skip...")
        #brain_proc.communicate()

        logger.info("Start main process")
        main_proc = subprocess.Popen(
            ["python", "%s/core/main.py" % settings.ROBOT_DIR]
        )

        if settings.SPEECH_RECOGNITION_ENABLED:
            #start julius
            logger.info('Start julius recognition service.')
            #julius_proc = subprocess.Popen(
                ##["julius", "-quiet", "-input", "mic"
                #, "-C" ,"%s/core/lib/julius/julian.jconf"
                #% settings.ROBOT_DIR , "-module"]
                #["padsp", "julius", "-quiet", "-input",
                #"mic", "-C" ,"%s/core/lib/julius/julian.jconf"
                #% settings.ROBOT_DIR , "-module"]
            #)

            #start julius connector
            jupid = process_exists('julius/connect.py')
            if not jupid:
                logger.info('Start julius connector '
                            + "%s/core/lib/julius/connect.py"
                            % settings.ROBOT_DIR)
                julius_conn_proc = subprocess.Popen(
                    ["python", "%s/core/lib/julius/connect.py"
                     % settings.ROBOT_DIR]
                )
                ##logger.debug("process id: %s"
                #, julius_conn_proc.communicate()[0])
                #julius_conn_proc.communicate()
                #logger.debug("process id: %s"
                #, julius_conn_proc.communicate()[0])
            else:
                logger.info('Julius connector is already running, skip...')

        #ask via jabber first
        apid = subprocess.Popen(
            ["python", "%s/core/brain/ask.py"
                % settings.ROBOT_DIR]
        )
        #run main process
        main_proc.communicate()

    except KeyboardInterrupt:
        #dpid = process_exists('source_direction')
        #logger.info( 'Stop sound source detector %s ', dpid )
        #os.kill(int(dpid), signal.SIGHUP)

        jpid = process_exists('jabber/connect.py')
        logger.info('Terminate jabber connector process  %s ', jpid)
        os.kill(int(jpid), signal.SIGHUP)

        jmpid = process_exists('jabber/mucbot.py')
        logger.info('Terminate jabber multiuser chat bot process  %s ', jmpid)
        os.kill(int(jmpid), signal.SIGHUP)

        jupid = process_exists('julius/connect.py')
        logger.info('Terminate julius connector process %s ', jupid)
        os.kill(int(jupid), signal.SIGHUP)

        ipid = process_exists('init.py')
        logger.info('Terminate main %s ', ipid)
        os.kill(int(ipid), signal.SIGHUP)

        bpid = process_exists('brain/listener.py')
        logger.info('Terminate brain listener process  %s ', bpid)
        os.kill(int(bpid), signal.SIGHUP)

        opid = process_exists('core/output.py')
        logger.info('Terminate output process  %s ', opid)
        os.kill(int(opid), signal.SIGHUP)

        apid = process_exists('brain/ask.py')
        logger.info('Terminate ask process  %s ', apid)
        os.kill(int(apid), signal.SIGHUP)
