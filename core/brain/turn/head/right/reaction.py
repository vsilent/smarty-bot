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





class Reaction:

    def __str__(self):
        """ """
        return 'This class provides .... '

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


    def continue_dialog(self):
        """ False will stop dialog after processing run() method  and start new from begining
            otherwise will continue to store request
        """
        return True

    #this method will be executed by default
    def run(self, request):
        """default method that will be executed by /core/brain/main.py and receives request string"""
        from core.device.neck.motor import StepperMotor2
        motor2 = StepperMotor2()
        motor2.rotate(-1, 15)
        motor2.reset_port()
        return True
