#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os

app_dir = os.path.normpath(os.path.join(os.getcwd(),
                                        os.path.dirname(__file__)))
sys.path.append(os.path.dirname(app_dir))
sys.path.append(os.path.dirname(app_dir) + '/../')

from core.config import settings
from core.config.settings import logger
import subprocess
import signal


def process_exists(process):
    """docstring for process_exists"""
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
        if settings.JABBER_ENABLED:
            # start jabber
            jpid = process_exists('jabber/connect.py')
            if not jpid:
                logger.info('Start jabber connector subprocess '
                            + "%s/core/lib/jabber/connect.py"
                            % settings.ROBOT_DIR)
                jabber_proc = subprocess.Popen(
                    ["python", "%s/core/lib/jabber/connect.py"
                     % settings.ROBOT_DIR]
                )
            else:
                logger.info('Jabber connector is already running, skip...')

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
        sid = process_exists('core/scheduler/at.py')
        if not sid:
            logger.info("Start scheduler subprocess")
            sched_proc = subprocess.Popen(
                ["python", "%s/core/scheduler/at.py" % settings.ROBOT_DIR]
            )
        else:
            logger.info("Scheduler subprocess already running, skip...")

        scid = process_exists('core/scheduler/connect.py')
        if not scid:
            logger.info("Start scheduler connector subprocess")
            schedc_proc = subprocess.Popen(
                ["python", "%s/core/scheduler/connect.py" % settings.ROBOT_DIR]
            )
        else:
            logger.info("Scheduler connector subprocess already running, skip...")

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

        # run main process
        main_proc.communicate()

    except KeyboardInterrupt:


        # dpid = process_exists('source_direction')
        # logger.info( 'Stop sound source detector %s ', dpid )
        # os.kill(int(dpid), signal.SIGHUP)

        sid = process_exists('scheduler/at.py')
        logger.info('Terminate scheduller connector process  %s ', sid)
        os.kill(int(sid), signal.SIGHUP)

        scid = process_exists('scheduler/connect.py')
        logger.info('Terminate scheduler connector process  %s ', scid)
        os.kill(int(scid), signal.SIGHUP)

        jpid = process_exists('jabber/connect.py')
        logger.info('Terminate jabber connector process  %s ', jpid)
        os.kill(int(jpid), signal.SIGHUP)

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
