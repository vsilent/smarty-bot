
#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Author: vs@webdirect.md
Description: Very simple reminder

"""
from core.people.person import Profile, Session
#from core.utils.utils import text2int
import re
from core.config.settings import logger, ROBOT_DIR
from datetime import datetime, timedelta
from core.scheduler.connect import add_job
from core.broadcast import say


class Reaction(object):
    """remind me with ..... at specific time reaction"""
    response = ''
    request = ''

    def __str__(self):
        return 'Remind me with ... at time reaction'

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

        skip_other = False
        sess = Session()
        sender = self.req_obj.get('sender', '')
        minute = 0
        sec = 0
        #exctract sender email
        email = sender.split('/')[0]
        #find user profile by primary email
        profile = sess.query(Profile).filter(Profile.email == email).one()
        req = self.request.replace('remind me with', '', 1)
        response = 'Ok. Scheduled.'

        #rest = ''
        msg = ''
        m = re.search('message\s+?([^at]+)', req.strip())

        if m and m.group(2):
            msg = m.group(2)
        else:
            ################################################
            #   at 10:00
            ################################################
            m = re.search('(.+)at\s?(\d{1,2})[:|\s](\d{1,2})', req)

            if m and m.group(1) and m.group(2) and m.group(3):
                msg = m.group(1)
                hour = m.group(2)
                minute = m.group(3)
                skip_other = True

            if not skip_other:
                ################################################
                # check  at 10 o'clock
                ################################################
                m = re.search("(.+)at\s?(\d{1,2})[:|\s](\d{1,2})\so'clock", req)
                if m and m.group(1) and m.group(2) and m.group(3):
                    msg = m.group(1)
                    hour = m.group(2)
                    minute = m.group(3)
                    skip_other = True
                else:
                    response = 'This a reminder. Unfortunatelly' + \
                            'I could not parse your message, ' + \
                            'but I guess you can remember what you wanted to do.'

        command = [
            'python',
            '%s/core/cron/cronjob.py' % ROBOT_DIR,
            '--uuid=%s' % profile.uuid,
            '--cmd=send jabber message',
            '--arguments=%s' % msg.replace('"', '')]

        logger.info('Going to add a new job')

        add_job(command, hour, minute, sec)

        if self.req_from == 'jabber':
            todo = {
                'text': response,
                'jmsg': response,
                'type': 'response'
            }
            self.response = todo
        elif self.req_from == 'julius':
            todo = {
                'say': response,
                'text': response,
                'type': 'response'
            }
            self.response = say(self.request.replace('say', '').upper())

        return self.response
