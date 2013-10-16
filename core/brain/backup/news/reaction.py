#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Author:
Description:
'''
from core.broadcast import say, bang
#from core.config.settings import logger
from core.people.person import Profile, Session
from crontab import CronTab
from getpass import getuser
from core.config.settings import ROBOT_DIR


class Reaction:
    """class Reaction"""
    response = ''
    request = ''

    def __str__(self):
        return 'Subscribing on News about "backup"'

    @classmethod
    def __init__(self, *args, **kwargs):
        """ original request string """
        #logger.info(args)
        #logger.info(kwargs)
        #logger.info(kwargs.get('req_obj'))

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

        #exctract sender email
        email = sender.split('/')[0]

        #find user profile by primary email
        profile = sess.query(Profile).filter(
            Profile.email == email).one()

        cron = CronTab(getuser())

        job = cron.new(
            command='/usr/bin/python %s/core/cron/cronjob.py\
            --uuid=%s --cmd="what people say about backup in twitter" \
            ' % (ROBOT_DIR, profile.uuid))
        job.minute.on(0)
        cron.write()

        response = 'Ok. You have been subscribed to news about Backup.'

        if self.req_from == 'jabber':
            todo = {'text': response, 'jmsg': response, 'type': 'response'}
            self.response = todo

        if self.req_from == 'julius':
            bang()
            todo = {'say': response, 'text': response, 'type': 'response'}
            self.response = say(self.request.replace('say', '').upper())

        return self.response
