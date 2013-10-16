#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Author: vs@webdirect.md
Description: Show all cronjobs for current client

'''
from core.people.person import Profile, Session
from crontab import CronTab
from getpass import getuser


class Reaction:
    """Show all cronjobs for current client"""
    response = ''
    request = ''

    def __str__(self):
        return 'Show all cronjobs for current client'

    @classmethod
    def __init__(self, *args, **kwargs):
        """ original request string """
        #get request object
        self.req_obj = kwargs.pop('req_obj')
        #request word sequence
        self.request = self.req_obj.get('request', '')
        #request received from (julius, jabber any other resources)
        self.req_from = self.req_obj.get('from', '')
        #get command history
        self.cmd_stack = kwargs.pop('cmd_stack', '')

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
        cron = CronTab(getuser())
        response = ''
        todo = {}

        for j in cron:
            if profile.uuid in j.render():
                response += j.render()
                continue
        if len(response) == 0:
            response = 'You have no cronjobs yet, you can add with command: \
                    *remind me every day at 10:00 with message "Do not forget\
                    to drink coffee"* '

        if self.req_from == 'jabber':
            todo['text'] = response
            todo['jmsg'] = response
            todo['type'] = 'response'
            self.response = todo

        if self.req_from == 'julius':
            from core.broadcast import say, bang
            bang()
            todo['type'] = 'response'
            todo['say'] = response
            self.response = say(self.request.replace('say', '').upper())

        return self.response
