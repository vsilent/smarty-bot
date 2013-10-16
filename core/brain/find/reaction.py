#!/usr/bin/env python
# -*- coding: utf-8 -*-

from core.people.requests import search_users_request
from core.people.person import Profile, Session


class Reaction:
    """class Reaction"""
    response = ''
    request = ''

    def __str__(self):
        return 'My new reaction'

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

        sender = self.req_obj.get('sender', '')
        uuid = self.req_obj.pop('uuid', '')
        profile = None
        sess = Session()
        req = self.request.replace('find ', '', 1).strip()

        #exctract sender email
        if sender:
            email = sender.split('/')[0]
            #find user profile by primary email
            profile = sess.query(Profile).filter(
                Profile.email == email).one()
            uuid = profile.uuid

        if uuid:
            #find user profile by uuid
            profile = sess.query(Profile).filter(
                Profile.uuid == uuid).one()

        if not profile:
            return {'text': 'unathorized',
                    'jmsg': 'unathorized',
                    'type': 'response'}

        response = search_users_request(req, uuid)

        if self.req_from == 'jabber':
            todo = {'text': response,
                    'jmsg': response,
                    'type': 'response'}
            self.response = todo

        return self.response
