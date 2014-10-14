#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Author:
Description:
'''
from core.broadcast import say, bang
from core.people.person import Profile, ProfileRequest, Session


class Reaction:
    """class Reaction"""
    response = ''
    request = ''

    def __str__(self):
        return 'My new reaction'

    @classmethod
    def __init__(self, *args, **kwargs):
        """ original request string """

        # get request object
        self.req_obj = kwargs.pop('req_obj')

        # request word sequence
        self.request = self.req_obj.get('request', '')

        # request received from (julius, jabber any other resources)
        self.req_from = self.req_obj.get('from', '')

        self.response = ''

    @classmethod
    def run(self):
        """default method"""

        email = None
        sess = Session()
        sender = self.req_obj.get('sender', '')

        # exctract sender email
        if sender:
            email = sender.split('/')[0]

        uuid = self.req_obj.pop('uuid', '')

        if email:
            # find user profile by primary email
            profile = sess.query(Profile).filter(Profile.email == email).one()
        elif uuid:
            # find user profile by uuid
            profile = sess.query(Profile).filter(Profile.uuid == uuid).one()

        hs = sess.query(ProfileRequest).order_by('id desc').limit(10)

        response = ''
        requests = [h.request for h in hs]

        if requests:
            response = "\n".join(requests)

        #########################################
        # If reaction executed by jabber client #
        #########################################

        if self.req_from == 'jabber':
            todo = {'text': response, 'jmsg': response, 'type': 'response'}
            self.response = todo

        #########################################
        # If reaction executed by julius client #
        #########################################

        if self.req_from == 'julius':
            bang()
            todo = {'say': response, 'text': response, 'type': 'response'}
            self.response = say(self.request.replace('say', '').upper())

        return self.response
#n = Reaction(*{'reserved':''}, **{'req_obj':{'from':'', 'request':''}})
#n.run()
