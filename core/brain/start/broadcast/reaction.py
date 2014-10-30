#!/usr/bin/env python
# -*- coding: utf-8 -*-

#  Some suggestions
#  ========================================
#
#
#  You can access main configuration module or better create your own in the
#  config module:
#
#  from core.config.settings import DEMO_MUSIC_DIR
#
#
#  Simple say command example:
#  ========================================
#
#  from core.output import say
#  say('OK')
#
#  Use subprocess module for your application:
#  ========================================
#
#  import subprocess
#  s = subprocess.Popen(['ffmpeg', '-i', speech, flac ] , stderr=subprocess.STDOUT, stdout=subprocess.PIPE).communicate()[0]
#
#
#
#  Use logging module instead of print
#
#  import logging
#  logging.debug('Playing... ')
#
# Put comments and suggest something here
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
import subprocess

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

        """default method that will be executed by /core/brain/main.py and receives request string"""

        response = 'You are not allowed to send broadcast messages.'
        email = None
        sender = self.req_obj.get('sender', '')

        if sender:
            email = sender.split('/')[0]
            sess = Session()
            #exctract uuid
            uuid = self.req_obj.pop('uuid', '')

            if email:
                #find user profile by primary email
                profile = sess.query(Profile).filter(Profile.email == email).one()
            elif uuid:
                #find user profile by uuid
                profile = sess.query(Profile).filter(Profile.uuid == uuid).one()
            else:
                response = 'Can not authenticate your id, are you registered ?'
                return { 'text' : response, 'jmsg' : response, 'type': 'response' }

        if profile.type  != 'admin':
            return { 'text' : response, 'jmsg' : response, 'type': 'response' }

        logger.info('Start video broadcasting...')
        proc = subprocess.Popen(
            ["motion"]
            #,shell=False
            #,stdin=subprocess.PIPE
            #,stdout=subprocess.PIPE
            #,stderr=subprocess.PIPE
        )
        #output, err = proc.communicate()
        #logger.info("%s ", output)
        #logger.info("%s", err)

        response  = 'Camera on.'

        if self.req_from == 'jabber':
            todo = { 'text' : response, 'jmsg' : response, 'type': 'response' }
            self.response = todo

        if self.req_from == 'julius':
            bang()
            todo = { 'say': response , 'text' : response ,'type': 'response' }
            self.response = say(self.request.replace('say', '').upper())

        return self.response

#direct test
#r = Reaction(**{'req_obj':{'request': '', 'from' : '','sender': 'your.name@gmail.com' }})
#r.run()
