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
from core.config import settings
from core.config.settings import logger
from core.utils.network.ping import pinger
from core.people.person import Profile, ProfileLink, Session
from core.lib.jabber.send_msg import SendMsgBot


class Reaction:
    """class Reaction"""
    response = ''
    request = ''

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

        email = None
        sess = Session()
        sender = self.req_obj.get('sender', '')

        #exctract sender email
        if sender:
            email = sender.split('/')[0]

        uuid = self.req_obj.pop('uuid', '')

        if email:
            #find user profile by primary email
            profile = sess.query(Profile).filter(Profile.email == email).one()
        elif uuid:
            #find user profile by uuid
            profile = sess.query(Profile).filter(Profile.uuid == uuid).one()

        hs = sess.query(ProfileLink).filter(
            ProfileLink.uuid == profile.uuid).all()

        hosts = [h.url.replace('https://', '').replace('http://', '') for h in hs]

        if hosts:
            response = "\n".join(hosts)
        else:
            response = 'you have to add url by command: add url http://mysite.com'

        #########################################
        # If reaction executed by jabber client #
        #########################################

        if self.req_from == 'jabber':
            todo = {'text': response, 'jmsg': response, 'type': 'response'}
            self.response = todo

        #########################################
        # If reaction executed by julius client #
        #########################################

        if self.req_from == 'julius':
            bang()
            todo = {'say': response, 'text': response, 'type': 'response'}
            self.response = say(self.request.replace('say', '').upper())

        return self.response
#n = Reaction(*{'reserved':''}, **{'req_obj':{'from':'', 'request':''}})
#n.run()
