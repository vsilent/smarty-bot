#!/usr/bin/env python
# -*- coding: utf-8 -*-


class Reaction:
    """class Reaction"""
    def __str__(self):
        return 'Reaction on exit'

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
        """ False will stop dialog after processing run()
        method  and start new from begining
            otherwise will continue to store request
        """
        return False

    @classmethod
    def run(self, request):
        """default method"""
        import logging
        from core.output import say
        msg = 'Stop, Application By Your Command'
        logging.debug('Saying... ' + msg)
        say(msg)
        import time
        time.sleep(2)
