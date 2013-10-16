#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Author: vs@webdirect.md
Description: how to use completion

'''
from core.people.person import Profile, Session
from core.config.settings import logger, ROBOT_DIR


class Reaction:
    """remind me every ...  reaction"""
    response = ''
    request = ''

    def __str__(self):
        return 'Remind me every ... reaction'

    @classmethod
    def __init__(self, *args, **kwargs):
        """ original request string """
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
        subdir = ROBOT_DIR.child('core', 'brain', 'remind', 'me')
        logger.info(subdir)

        #exctract sender email
        email = sender.split('/')[0]

        #find user profile by primary email
        profile = sess.query(Profile).filter(Profile.email == email).one()
        response = ''
        if profile:
            response = profile.first_name + ', '
            pass

        response += "how do you want to be reminded ?\nHere are some examples of how you can set a reminder:\n"
        l = [" ".join(p.format().split('/')[2:]) for p in subdir.relative().listdir() if p.isdir()]
        response += "\n".join(l)

        if self.req_from == 'jabber':
            todo = {'text': response, 'jmsg': response, 'type': 'response'}
            self.response = todo

        if self.req_from == 'julius':
            from core.broadcast import say, bang
            bang()
            todo = {'say': response, 'text': response, 'type': 'response'}
            self.response = say(self.request.replace('say', '').upper())

        return self.response
