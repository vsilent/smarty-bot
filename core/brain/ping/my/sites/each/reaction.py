
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
#         fulldate = datetime.now().strftime("%A, %d. %B %Y %I:%M%p")
#
#         hours = datetime.now().strftime("%I")
#         minutes = datetime.now().strftime("%I")
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
Author:
Description:
'''
from core.broadcast import say, bang
from core.config.settings import logger, ROBOT_DIR
from core.utils.network.ping import pinger
from core.people.person import Profile,ProfileLink, Session
import re
from crontab import CronTab

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

        cron = CronTab('smarty')
        job  = cron.new( command='/usr/bin/python %s/cron/cronjob.py --uuid=%s --cmd="ping my sites"' % ( ROBOT_DIR, profile.uuid ))

        hour = re.search('(\d+)(\s+)?[hours?|h]', self.request)

        if hour:
            job.hour.every(found.group(1))

        else:
            min = re.search('(\d+)(\s+)?[minutes?|min|m]', self.request)
            if min:
                job.hour.every(found.group(1))

        if 'day' == self.request.trim():
            job.dow.every()

        if 'month' == self.request.trim():
            job.month.every()

        if 'hour' == self.request.trim():
            job.hour.every()

        if 'minute' == self.request.trim():
            job.minute.every()

        #And setting the job's time restrictions:
        #job.minute.during(5,50).every(5)

        #job.dow.on('SUN')
        #job.month.during('APR', 'NOV')

        cron.write()
        logger.info('adding cronjob %s' %  cron.render() )


        #cron.remove_all( 'echo' )
        #cron.write()
        response = 'ok, cronjob added %s' % cron.render()


        if self.req_from == 'jabber':
            todo = { 'text' : response, 'jmsg' : response, 'type': 'response' }
            self.response = todo

        if self.req_from == 'julius':
            bang()
            todo = { 'say': response , 'text' : response ,'type': 'response' }
            self.response = say(self.request.replace('say', '').upper())

        return self.response


#n = Reaction(*{'reserved':''}, **{'req_obj':{'from':'', 'request':''}})
#n.run()
