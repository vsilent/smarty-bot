#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Author: vs@webdirect.md
Description: Delete last cronjob command

'''
#from core.people.person import Profile, Session
#from core.utils.sys.report import report_bug
from core.config import settings
import re
#import sys


class Reaction:
    """Delete last cronjob command"""
    response = ''
    request = ''

    def __str__(self):
        return 'Delete last cronjob command'

    @classmethod
    def __init__(self, *args, **kwargs):
        """ original request string """
        #get request object
        self.req_obj = kwargs.pop('req_obj')

        #request word sequence
        self.request = self.req_obj.get('request', '')

        #request received from (julius, jabber any other resources)
        self.req_from = self.req_obj.get('from', '')

        #get command history
        self.cmd_stack = kwargs.pop('cmd_stack', '')
        self.cmd_args = kwargs.pop('cmd_args', '')

        self.response = ''

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

        req = re.compile(r'^' + settings.MY_NAME, flags=re.IGNORECASE)
        res = req.sub("", self.request.strip()).split()

        todo = {}
        args = []
        req_obj = {}

        has_req = len(filter(None, res)) != 0

        if has_req:
            args = filter(lambda word: word not in ['!', ',', '.', '..'], res)

        if not has_req:
            response = 'Yes? Any commands?'
            req_obj['request'] = " ".join(args)
            req_obj['type'] = 'response'
            req_obj['from'] = self.req_from
            todo['text'] = response
            todo['jmsg'] = response
        else:
            response = 'ok'
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
            from core.broadcast import say, bang
            bang()
            todo['type'] = 'response'
            todo['say'] = response
            self.response = say(self.request.replace('say', '').upper())

        return self.response
