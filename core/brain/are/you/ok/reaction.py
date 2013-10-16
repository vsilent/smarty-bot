#!/usr/bin/env python
# -*- coding: utf-8 -*-

#from core.config.settings import logger
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
        req_obj = kwargs.pop('req_obj')
        self.request = req_obj.get('request', '')
        #request from (julius, jabber any other resources)
        self.req_from = req_obj.get('from', '')
        self.response = ''

    @classmethod
    def continue_dialog(self):
        """ False will stop dialog after processing run() method  and start new from begining
            otherwise will continue to store request
        """
        return True

    #this method will be executed by default
    @classmethod
    def run(self):
        """default method that will be executed by /core/brain/main.py and receives custom request string / command arguments"""
        if self.req_from == 'jabber':
            response = 'yes, Im fine'
            self.response = {'text': response, 'jmsg': response}
        return self.response
