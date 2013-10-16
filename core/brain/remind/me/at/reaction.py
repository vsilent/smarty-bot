#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Author: vs@webdirect.md
Description: Very simple reminder

'''
from core.people.person import Profile, Session
#from core.utils.utils import text2int
import re
from core.config.settings import logger, ROBOT_DIR
from subprocess import Popen, PIPE


class Reaction:
    """remind me at specific time reaction"""
    response = ''
    request = ''

    def __str__(self):
        return 'Remind me at ... reaction'

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

        skip_other = False
        sess = Session()
        sender = self.req_obj.get('sender', '')

        #exctract sender email
        email = sender.split('/')[0]

        #find user profile by primary email
        profile = sess.query(Profile).filter(Profile.email == email).one()

        req = self.request.replace('remind me', '', 1)

        if req.strip().startswith('at'):
            ################################################
            #   at 10 o'clock
            ################################################
            time = re.search("[^0-9](\d{1,2})\so'clock", req)
            if time and time.group(1):
                hour = time.group(1)
                #min = '00'
                skip_other = True

            if not skip_other:
            ################################################
            #   at 10:00
            ################################################
                time = re.search('[^0-9](\d{1,2}):(\d{2})[^0-9]', req)
                if time and time.group(1) and time.group(2):
                    min = time.group(2)
                    hour = time.group(1)
                    skip_other=True

            m = re.search('(by|with|to|of)\s+message\s+?(.+)', req.strip())

            if m and m.group(2):
                msg = m.group(2)
            else:
                m = re.search('\s+?(by|with|to|of)\s+?(.+)', req)
                if m and m.group(2):
                    msg = m.group(2)
                else:
                    msg = 'This a reminder. Unfortunatelly I could not parse your message, \
                            but I guess you can remember what you wanted to do.'

            logger.info(msg)
            command = ['python',
                       '%s/core/cron/cronjob.py' % ROBOT_DIR,
                       '--uuid=%s' % profile.uuid,
                       '--cmd="send jabber message"',
                       '--arguments="%s"' % msg.replace('"', '')]

            #output=`python  | grep hda`
            # becomes
            p1 = Popen(command, stdout=PIPE)
            #p2 = Popen(["at", "now + 1 minute"], stdin=p1.stdout, stdout=PIPE)
            p2 = Popen(["at", "now + 1 minute"],
                       stdin=p1.stdout,
                       stdout=PIPE,
                       shell=True)
            p1.stdout.close()  # Allow p1 to receive a SIGPIPE if p2 exits.
            p2.communicate()[0]
        #logging.info('Start subprocess...')
        #stdoutdata, stderrdata = proc.communicate()
        #echo notify-send "hi" | at 00:06
        #echo notify-send "hi" | at 00:06
