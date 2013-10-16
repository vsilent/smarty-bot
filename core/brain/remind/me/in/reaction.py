#!/usr/bin/env python
# -*- coding: utf-8 -*-

#  Example
#  =============================================================================
#
#
#  You can access main configuration module or better create your own in the
#  config module:
#
#  from core.config.settings import DEMO_MUSIC_DIR
#
#
#  Simple command example:
#  =============================================================================
#  =============================================================================
#
# from core.config.settings import logger
# from core.broadcast import output
#
# class Reaction:
#     """class Reaction"""
#     def __str__(self):
#         return 'My cool reaction module'
#
#    def __init__(self, *args, **kwargs):
#         """ original request string """
#         self.request = kwargs.pop('req_obj')['request']
#         self.response = None
#
#     def run(self):
#         """default method that executes by /core/brain/main.py and receives request string"""
#         #use subprocess for your bindings when develop a new functionality
#         from datetime import datetime
#         fulldate = datetime.utcnow().strftime("%A, %d. %B %Y %I:%M%p")
#
#         hours = datetime.utcnow().strftime("%I")
#         minutes = datetime.utcnow().strftime("%I")
#
#         #logger.info('worker got request %s' % self.request)
#
#         if self.request['from'] == 'jabber':
#             todo = { 'text' : fulldate, 'jmsg' : fulldate }
#
#         if self.request['from'] == 'julius':
#             todo = { 'say': "IT'S, %d O'CLOCK AND %d MINUTES" % ( int(hours), int(minutes)),
#                     'text' : fulldate }
#
#         self.response = todo
#         return self.response
#
#
#  Use subprocess module for your application:
#  =============================================================================
#
#  This example will run external programm in daemon mode
#  import subprocess
#  s = subprocess.Popen(['ffmpeg', '-i', speech, flac ])
#
#
#  Use logging module instead of print
#
#  from core.config.settings import  logger
#  logger.debug('Playing... ')
#
#  Put comments and suggest something here
#
#
#
#  =============================================================================
#  Attention !  If you create new command please append it's name to
#  embedded_commands list in core/config/settings.py
#  like: embedded_commands = ['say', 'send', 'receive', 'my_new_command']]
#  Please, describe what functionality your extension provides in __str__ method
#  Comment your code
#  =============================================================================

'''
Author: vs@webdirect.md
Description: Very simple reminder

Remind me
remind me in
remind me within
remind me at
remind me after
remind me before
remind me during
remind me during
remind me each
remind me on next week
remind me on sunday
remind me tomorrow

similar:
inform me
notify me
msg me
message me
ping me
alert me

'''
from core.people.person import Profile,ProfileLink, Session
from core.utils.utils import text2int
import re
from crontab import CronTab
from getpass import getuser
from core.config.settings import logger, ROBOT_DIR

class Reaction:
    """class Reaction"""
    response = ''
    request  = ''

    def __str__(self):
        return 'My new reaction'

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
        profile = sess.query(Profile).filter(Profile.email == email).one()


        cron = CronTab(getuser())

        r = re.compile(re.escape('remind me in'), re.IGNORECASE)
        req = r.sub('', self.request)

        m = re.search('[by|with|to|of]\s+"?([^"]+)"?', req )

        if m:
            msg = m.group(1)
        else:
            msg = 'This a reminder. Unfortunatelly I could not parse your message, but I guess you can remember what you wanted to do'

        job  = cron.new( command='/usr/bin/python %s/cron/cronjob.py --uuid=%s --cmd="send jabber message %s"' % ( ROBOT_DIR, profile.uuid, msg ))


        if req.startswith('a month'):
            job.month.on()

        if req.startswith('an hour'):
            job.hour.on()

        if req.startswith('a minute'):
            job.minute.on(1)

        ################################################
        #   hours
        ################################################
        hour = re.search( '(\d+)(\s+)?[hours?|h]', req )
        if hour:
            job.hour.on(hour.group(1))

        else:
            #if hour presents in human word : one, two etc.
            hour = re.search('(.+?)\s+[hours?|h|hs]', req )
            if hour:
                job.hour.on(hour.group(1))



        ################################################
        #   hours
        ################################################
        day = re.search('(\d+)(\s+)?[days?|min|m]', req )
        if day:
            job.dow.on(day.group(1))
        else:
            #if day presents in human word : one, two etc.
            day = re.search('(.+?)\s+[days?|min|m]', req )
            if day:
                job.dow.on(day.group(1))

        ################################################
        #   minutes
        ################################################
        min = re.search('(\d+)(\s+)?[minutes?|min|m]', req )
        if min:
            job.minute.on(min.group(1))
        else:
            #if day presents in human word : one, two etc.
            min = re.search('(.+?)\s+[minutes?|mins?|m]', req )
            if min:
                job.minute.on(min.group(1))

        cron.write()

        logger.info('adding cronjob %s' %  cron.render() )
        response = 'ok, cronjob added %s' % cron.render()


        if self.req_from == 'jabber':
            todo = { 'text' : response, 'jmsg' : response, 'type': 'response' }
            self.response = todo

        if self.req_from == 'julius':
            from core.broadcast import say, bang
            bang()
            todo = { 'say': response , 'text' : response ,'type': 'response' }
            self.response = say(self.request.replace('say', '').upper())

        return self.response


#n = Reaction(*{'reserved':''}, **{'req_obj':{'from':'jabber', 'request':'remind me in 20 minutes with "hey don\'t forget about pizza"', 'sender': 'vasilii.pascal@gmail.com'}})

n = Reaction(*{'reserved':''}, **{'req_obj':{'from':'jabber', 'request':'remind me in 20 minutes with "hey don\'t forget about pizza"', 'sender': 'vasilii.pascal@gmail.com'}})
n.run()
