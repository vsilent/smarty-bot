#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Author: vs@webdirect.md
Description: Delete last cronjob command

'''
from core.people.person import Profile, Session
from crontab import CronTab
from getpass import getuser
from core.lib.wordprocessing.agree import agree
from core.utils.sys.report import report_bug
#from config.settings import logger


class Reaction:
    """Delete last cronjob command"""
    response = ''
    request = ''

    def __str__(self):
        return 'Delete last cronjob command'

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

        last = None
        for j in cron:
            if profile.uuid in j.render():
                last = j.render()
                continue

        if last:
            todo = {'continue': 1}
            response = 'did you mean this one %s ?' % last
        else:
            todo = {'continue': 1, 'error': 1}
            response = 'hmm, I could not find any of your cronjobs, if you are sure there were I can report a bug, should I report a bug to developers ? (y/n)'

        #cron.write()

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

    def on_continue(self, msg):
        """docstring for on_continue"""
        #print('nice, continue with:')

        request = msg.get('request', None)
        sender = msg.get('sender', '')
        req_from = msg.get('from', '')
        error = msg.get('error', '')
        #logger.info('error %s..........................' % error)
        #logger.info('req_from %s..........................' % req_from)
        #logger.info('request %s..........................' % request)

        sess = Session()

        #exctract sender email
        email = sender.split('/')[0]

        #find user profile by primary email
        profile = sess.query(Profile).filter(Profile.email == email).one()
        #logger.info('profile %s..........................' % profile)

        if error:
            #logger.info('report ..........................')
            if agree(request):
                report_bug('user %s can not find cronjobs ' % profile.uuid)
                response = 'ok, reported.. '
                response += 'by the way, you can add a reminder with command: *remind me every day at 10:00 with message "Do not forget to drink coffee"* '
            else:
                response = 'ok'
                response += ' by the way, you can add a reminder with command: \
                *remind me every day at 10:00 with message "Do not forget to drink coffee"* '

            self.response = {'text': response, 'jmsg': response, 'type': 'response', 'continue': 0}
            return self.response

        cron = CronTab(getuser())

        last = None
        for j in cron:
            if profile.uuid in j.render():
                last = j.render()
                continue

        if agree(request) and len(last) > 0:
            cron.remove(last)
            cron.write()
            response = 'ok, done'
        else:
            response = "ok"

        if req_from == 'jabber':
            todo = {'text': response, 'jmsg': response, 'type': 'response', 'continue': 0}
            self.response = todo

        if req_from == 'julius':
            from core.broadcast import say, bang
            bang()
            todo = {'say': response, 'text': response, 'type': 'response', 'continue': 0}
            self.response = say(self.request.replace('say', '').upper())

        return self.response
