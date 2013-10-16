#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Author: vs@webdirect.md
Description: Very simple reminder

'''
from core.people.person import Profile, Session
from crontab import CronTab
from getpass import getuser
from core.config.settings import logger, ROBOT_DIR


class Reaction:
    """remind me every ...  reaction"""
    response = ''
    request = ''

    def __str__(self):
        return 'Remind me every ... reaction'

    @classmethod
    def __init__(self, *args, **kwargs):
        """ original request string """
        #get request object
        self.req_obj = kwargs.pop('req_obj')

        #request word sequence
        self.request = self.req_obj.get('request', '')

        #request received from (julius, jabber any other resources)
        self.req_from = self.req_obj.get('from', '')

        self.response = ''

    @classmethod
    def run(self):
        """default method"""

        sess = Session()
        sender = self.req_obj.get('sender', '')

        #extract sender email
        email = sender.split('/')[0]

        #find user profile by primary email
        profile = sess.query(Profile).filter(Profile.email == email).one()

        cron = CronTab(getuser())
        command = self.request.replace('remind me every day with ', '', 1)

        job = cron.new(
            command='/usr/bin/python %s/core/cron/cronjob.py\
            --uuid=%s --cmd="%s"' % (ROBOT_DIR,
                                     profile.uuid,
                                     command.replace('"', '')))

        ################################################
        #   every day at 17:00
        ################################################
        job.minute.on(0)
        job.hour.on(17)
        job.dow.every()
        cron.write()

        logger.info('adding cronjob %s' % cron.render())
        #response = 'ok, added %s' % job.render()
        response = 'ok, done.'

        if self.req_from == 'jabber':
            todo = {'text': response, 'jmsg': response, 'type': 'response'}
            self.response = todo

        if self.req_from == 'julius':
            from core.broadcast import say, bang
            bang()
            todo = {'say': response, 'text': response, 'type': 'response'}
            self.response = say(self.request.replace('say', '').upper())

        return self.response
