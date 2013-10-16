#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Author:
Description:
'''


class Reaction:

    @classmethod
    def __str__(self):
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

    @classmethod
    def continue_dialog(self):
        """ False will stop dialog after processing
        run() method  and start new from begining
            otherwise will continue to store request
        """
        return True

    #this method will be executed by default
    @classmethod
    def run(self, request):
        """default method that will be executed by
        /core/brain/main.py and receives request string"""
        return True
