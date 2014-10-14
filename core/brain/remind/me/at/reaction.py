#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""

Author: vs@webdirect.md.

Description: Very simple reminder.

"""

from core.people.person import Profile, Session
from core.config.settings import MSG_ME
import re
from core.config.settings import logger, ROBOT_DIR
from core.scheduler.connect import add_job
from core.broadcast import say


class Reaction(object):
    """remind me at specific time reaction."""
    response = ''
    request = ''

    def __str__(self):
        return 'Remind me at ... reaction'

    @classmethod
    def __init__(self, *args, **kwargs):
        """ original request string """
        #get request object
        self.req_obj = kwargs.pop('req_obj')
        self.cmd_args = kwargs.pop('cmd_args', '')

        #request word sequence
        self.request = self.req_obj.get('request', '')

        #request received from (julius, jabber any other resources)
        self.req_from = self.req_obj.get('from', '')
        self.response = ''


    @classmethod
    def run(self):
        """default method."""

        error = False
        skip_other = False
        sess = Session()

        sender = self.req_obj.get('sender', '')
        uuid = self.req_obj.pop('uuid', '')

        if sender:
            #exctract sender email
            email = sender.split('/')[0]

        minute = 0
        sec = 0

        if email:
            #find user profile by primary email
            profile = sess.query(Profile).filter(Profile.email == email).one()
        elif uuid:
            #find user profile by uuid
            profile = sess.query(Profile).filter(Profile.uuid == uuid).one()

        time_str = self.cmd_args[0]
        rest_lst = self.cmd_args[1:]  # rest sentense list

        response = 'Ok. Scheduled.'

        ################################################
        #   at 10 o'clock
        ################################################
        time = re.search("[^0-9](\d{1,2})", time_str)
        if time and time.group(1) and ("o'clock" in rest_lst[0]):
            hour = time.group(1)
            minute = 0
            skip_other = True
            del rest_lst[0]

        if not skip_other:
        ################################################
        #   at 10:00
        ################################################
            time = re.search('(\d{1,2})[:|\s](\d{2})', time_str)
            if time and time.group(1) and time.group(2):
                minute = time.group(2)
                hour = time.group(1)
                skip_other = True

        msg = " ".join(rest_lst)

        for sent in MSG_ME:
            if sent in msg:
                msg.replace(sent, '')


        #m = re.search('(by|with|to|of)\s+message\s+?(.+)', req.strip())
        #if m and m.group(2):
            #msg = m.group(2)
        #else:
            #m = re.search('\s+?(by|with|to|of)\s+?(.+)', req)
            #if m and m.group(2):
                #msg = m.group(2)
            #else:
                #error = True
                #response = 'This a reminder. Unfortunatelly I could not parse your message, \
                        #but I guess you can remember what you wanted to do.'
        if not error:
            command = [
                'python',
                '%s/core/cron/cronjob.py' % ROBOT_DIR,
                '--email=%s' % profile.email,
                '--uuid=%s' % profile.uuid,
                '--cmd=send jabber message',
                '--arguments=%s' % msg.replace('"', '')
            ]
            add_job(command, hour, minute, sec)

        if self.req_from == 'jabber':
            todo = {'text': response, 'jmsg': response, 'type': 'response'}
            self.response = todo
        elif self.req_from == 'julius':
            todo = {'say': response, 'text': response, 'type': 'response'}
            self.response = say(self.request.replace('say', '').upper())

        return self.response
