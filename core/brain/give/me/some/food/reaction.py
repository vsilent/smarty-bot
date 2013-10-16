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
from core.config.settings import logger
from core.people.person import Profile, Session
from getpass import getuser
from core.lib.wordprocessing.agree import agree
from core.utils.sys.report import report_bug

class Reaction:
    """class Reaction"""
    response = ''
    request = ''

    def __str__(self):
        return 'Give me some food reaction'

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

        response = 'I can order you a pizza, would you like one ?'

        if self.req_from == 'jabber':
            todo = {'text': response, 'jmsg': response, 'type': 'response'}
            self.response = todo

        if self.req_from == 'julius':
            bang()
            todo = {'say': response, 'text': response, 'type': 'response'}
            self.response = say(self.request.replace('say', '').upper())


        return self.response

    def on_continue(self, msg):
        """docstring for on_continue"""
        request = msg.get('request', None)
        sender = msg.get('sender', '')
        req_from = msg.get('from', '')
        error = msg.get('error', '')
        sess = Session()
        #exctract sender email
        email = sender.split('/')[0]

        #find user profile by primary email
        profile = sess.query(Profile).filter(Profile.email == email).one()
        #logger.info('profile %s..........................' % profile)

        if error:
            #logger.info('report ..........................')
            if agree(request):
                response = 'ok'
            else:
                response = 'ok'

            self.response = {'text': response, 'jmsg': response, 'type': 'response', 'continue': 0}

        return self.response
#direct test
#r = Reaction(**{'req_obj':{'request': '', 'from' : '','sender': 'your.name@gmail.com' }})
#r.run()
