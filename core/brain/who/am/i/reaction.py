#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Author:
Description:
'''
from core.broadcast import say, bang
from core.people.person import Profile, Session
from core.response import Response


class Reaction:
    """class Reaction"""
    response = ''
    request = ''

    def __str__(self):
        return 'My new reaction'

    @classmethod
    def __init__(self, *args, **kwargs):
        """ original request string """
        # logger.info(args)
        # logger.info(kwargs)
        # logger.info(kwargs.get('req_obj'))
        self.req_obj = kwargs.pop('req_obj')
        self.request = self.req_obj.get('request', '')
        self.req_from = self.req_obj.get('from', '')
        self.response = ''

    @classmethod
    def run(self):
        """default method"""

        sender = self.req_obj.get('sender', '')
        if sender == '':
            if self.req_from in ['web', 'jabber']:
                self.response = Response(
                    html='You should be authorized. Please log in.'
                )
                return self.response

        email = sender.split('/')[0]
        sess = Session()
        profile = sess.query(Profile).filter(Profile.email == email).one()

        # logger.info('%s' % profile.email)
        # logger.info('%s' % profile.uuid)
        # logger.info('%s' % profile.first_name)

        if profile.first_name:
            response = 'You are %s %s' % (
                profile.first_name, profile.last_name
            )
        else:
            response = """You are known as %s.
            But it would be realy nice if you present yourself :).
            What is your full name ?""" % email

        if self.req_from == 'jabber':
            self.response = Response(text=response)

        if self.req_from == 'julius':
            bang()
            self.response = say(self.request.replace('say', '').upper())

        return self.response
