#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Author: vs@webdirect.md
Description: Delete last_command cronjob command

'''
from core.people.person import Profile, Session
from core.lib.wordprocessing.agree import agree
from core.utils.sys.report import report_bug
from config.settings import logger


class Reaction:
    """Delete last_command cronjob command"""
    response = ''
    request = ''

    def __str__(self):
        return 'Delete last_command cronjob command'

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
        uuid = self.req_obj.get('uuid', '')

        #exctract sender email
        if sender:
            email = sender.split('/')[0]
            if email:
                #find user profile by primary email
                self.profile = sess.query(Profile).filter(
                    Profile.email == email).one()
        elif uuid:
            #find user profile by uuid
            self.profile = sess.query(
                Profile).filter(Profile.uuid == uuid).one()

        last_command = self.cmd_stack[-2]
        if last_command:
            todo = {'continue': 1}
            response = 'did you mean this one "*%s*" ? ' % last_command
        else:
            todo = {'continue': 1, 'error': 1}
            response = 'hmm, I could not find any of your previous command'

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

    @classmethod
    def on_continue(self, msg):
        """docstring for on_continue"""
        #print('nice, continue with:')

        request = msg.get('request', None)
        sender = msg.get('sender', '')
        uuid = msg.get('uuid', '')
        req_from = msg.get('from', '')
        error = msg.get('error', '')
        #logger.info('error %s.....................' % error)
        #logger.info('req_from %s..................' % req_from)
        #logger.info('request %s...................' % request)
        #logger.info('uuid %s......................' % uuid)

        sess = Session()
        last_command = self.cmd_stack[-2]

        #exctract sender email
        if sender:
            email = sender.split('/')[0]
            if email:
                #find user profile by primary email
                self.profile = sess.query(Profile).filter(
                    Profile.email == email).one()
        elif uuid:
            #find user profile by uuid
            self.profile = sess.query(
                Profile).filter(Profile.uuid == uuid).one()

        if error:
            if agree(request):
                report_bug('no prev commands found for %s' % self.profile.uuid)
                response = 'ok, reported.. '
            else:
                response = 'ok'

            self.response = {
                'text': response,
                'jmsg': response,
                'type': 'response',
                'continue': 0}

            return self.response

        if agree(request) and len(last_command) > 0:
            #repeat last_command command here
            response = 'ok, got it.. one moment'
            logger.info('going to repeat %s' % last_command)

            self.response = {
                'req_obj': {
                    'request': last_command,
                    'from': req_from,
                    'sender': sender,
                    'uuid': uuid,
                    'type': 'request',
                    'continue': 1
                },
                'jmsg': response,
                'text': response,
                'type': 'response',
                'continue': 1
            }
            return self.response
        else:
            response = "ok"

        todo = {'text': response,
                'jmsg': response,
                'type': 'response'}

        if req_from == 'jabber':
            self.response = todo

        if req_from == 'julius':
            from core.broadcast import say, bang
            bang()
            todo = {'say': response,
                    'text': response,
                    'type': 'response',
                    'continue': 0}
            self.response = say(self.request.replace('say', '').upper())

        return self.response
