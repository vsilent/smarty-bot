#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" apscheduler.  """

import subprocess
from apscheduler.scheduler import Scheduler
from apscheduler.jobstores.shelve_store import ShelveJobStore
from datetime import date, datetime, timedelta
import os
import shelve
import zmq
from core.config.settings import logger


def job(command):
    #""" docstring for job. """
    subprocess.Popen(command)


class ScheduleDaemon(object):

    response = None

    """
    scheduler - at daemon.

    one of daemons

    """

    def __init__(self, name="scheduler-at"):
        """docstring for __init__"""
        self.context = zmq.Context()
        self.name = name
        self.sock = self.context.socket(zmq.REP)
        self.sock.bind('ipc:///tmp/smarty-%s' % name)


    def add_job(self, command, hour, minute, sec=0):

        logger.info("2. scheduler adding job command: %s at %s:%s:%s" % (
            command, hour, minute, sec
        ))
        sched = Scheduler(standalone=True)

        #make a db file
        shelve.open(
            os.path.join(
                os.path.dirname(__file__),
                'example.db'
            )
        )
        sched.add_jobstore(ShelveJobStore('example.db'), 'shelve')

        exec_time = datetime(
            date.today().year,
            date.today().month,
            date.today().day,
            int(hour),
            int(minute),
            int(sec)
        )
        #test
        #exec_time = datetime.now() + timedelta(seconds=5)

        sched.add_date_job(
            job,
            exec_time,
            name='alarm',
            jobstore='shelve',
            args=[command]
        )
        sched.start()


    def start(self):
        """ start """

        logger.info('daemon %s started successfully' % (self.name))
        while True:
            self.msg = self.sock.recv_json()

            logger.info('daemon %s received %s' % (self.name, self.msg))
            self.cmd = self.msg.get('cmd', None)

            if self.cmd == 'terminate':
                self.response['text'] = 'terminated'
                self.sock.send_json(self.response)
                self.sock.close()
                self.context.term()
                break
            if self.cmd:
                response = self.process_command(self.cmd)
                logger.info('daemon responded with %s' % response)
        exit()

    def process_command(self, cmd):
        """docstring for process"""

        if cmd == 'add_job':
            err = 'uhm, I did not understand.'
            response = {'text': ';-)'}
            command = self.msg.pop('command', None)
            hour = self.msg.pop('hour', None)
            minute = self.msg.pop('minute', None)
            sec = self.msg.pop('sec', None)
            self.sock.send_json({'text': 'job added'})

            try:
                response = self.add_job(command, hour, minute, sec)
            except (KeyboardInterrupt, SystemExit) as e:
                logger.exception(e)
                response = {'text': 'wrong params passed'}

            return response


daemon = ScheduleDaemon()
daemon.start()
