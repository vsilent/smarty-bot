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
    """Ping my sites every hour"""
    response = ''
    request = ''

    def __str__(self):
        return 'Ping my sites every hour reaction'

    @classmethod
    def __init__(self, *args, **kwargs):
        """ original request string """
        self.req_obj = kwargs.pop('req_obj')
        self.request = self.req_obj.get('request', '')
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
        profile = sess.query(Profile).filter(Profile.email == email).one()

        req = self.request.replace('ping my sites every hour', '', 1)
        msg = ''

        #by default 10:00
        if len(req.strip()) == 0:
            cron = CronTab(getuser())
            job = cron.new(command='/usr/bin/python %s/core/cron/cronjob.py --uuid=%s --cmd="ping my sites" --arguments="%s"' % (ROBOT_DIR, profile.uuid, msg.replace('"', '')))
            job.minute.on(0)
            job.hour.every(1)
            cron.write()
            logger.info('adding cronjob %s' % cron.render())
            response = 'ok, cronjob added %s' % str(job)

        if self.req_from == 'jabber':
            todo = {'text': response, 'jmsg': response, 'type': 'response'}
            self.response = todo

        if self.req_from == 'julius':
            from core.broadcast import say, bang
            bang()
            response = 'ok'
            todo = {'say': response, 'text': response, 'type': 'response'}
            self.response = say(self.request.replace('say', '').upper())

        return self.response

#n = Reaction(*{'reserved':''}, **{'req_obj':{'from':'jabber', 'request':'remind me every 2 minutes with "hey don\'t forget about pizza"', 'sender': 'vasilii.pascal@gmail.com'}})
#n.run()
