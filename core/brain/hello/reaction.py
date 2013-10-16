#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Author:
Description:
'''
from core.broadcast import say, bang
#from core.config.settings import logger
import re


class Reaction:
    """Hi Reaction"""
    response = ''
    request = ''

    def __str__(self):
        return 'Hi reaction'

    @classmethod
    def __init__(self, *args, **kwargs):
        """ original request string """
        #logger.info(args)
        #logger.info(kwargs)
        #logger.info(kwargs.get('req_obj'))

        #get request object
        req_obj = kwargs.pop('req_obj')

        #request word sequence
        self.request = req_obj.get('request', '')

        #request received from (julius, jabber any other resources)
        self.req_from = req_obj.get('from', '')

        self.response = ''

    #@classmethod
    #def run(self):
        #"""default method"""

        #if request.startswith(settings.GREETINGS) or(request.startswith('hi') and 'jabber' == self._initiator):
            #self.set_dialog_stage(1)
            ##try to remove greeting
            #for word in settings.GREETINGS:
                #if word in request:
                    #request = request.replace(word, '')
                    #break
            #self.response = {'text': 'Hi, any command ? type "help"', 'continue': 1, 'type': 'response'}
            #self.set_request_as_greeting()

            #if self._initiator == 'julius':
                #self.response['say'] = 'Hi'
                #output(req_obj)

            #return self.response
    @classmethod
    def run(self):
        """default method"""

        #sess = Session()
        #sender = self.req_obj.get('sender', '')

        #exctract sender email
        #email = sender.split('/')[0]

        #if email:
            ##find user profile by primary email
            #profile = sess.query(Profile).filter(Profile.email == email).one()
        #logger.info('Somebody says hi')

        req = re.compile(r'^hello', flags=re.IGNORECASE)
        res = req.sub("", self.request.strip()).split()

        todo = {}
        args = []
        req_obj = {}

        has_req = len(filter(None, res)) != 0

        if has_req:
            args = filter(lambda word: word not in ['!', ',', '.', '..'], res)

        if not has_req:
            response = 'Hi, any command? type "help"'
            req_obj['request'] = " ".join(args)
            req_obj['type'] = 'response'
            req_obj['from'] = self.req_from
            todo['text'] = response
            todo['jmsg'] = response
            todo['continue'] = 0
        else:
            response = 'Hi'
            req_obj['request'] = " ".join(args)
            req_obj['type'] = 'request'
            req_obj['from'] = self.req_from
            todo['req_obj'] = req_obj
            todo['continue'] = 1
            todo['text'] = response
            todo['jmsg'] = response

        if self.req_from == 'jabber':
            self.response = todo

        if self.req_from == 'julius':
            bang()
            todo['type'] = 'response'
            todo['say'] = response
            self.response = say(self.request.replace('say', '').upper())

        return self.response
