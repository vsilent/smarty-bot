#!/usr/bin/env python
# -*- coding: utf-8 -*-

from core.utils.network.tweet import tweet

'''
Author:
Description:
'''
from core.broadcast import say, bang
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
        self.args = kwargs.pop('cmd_args')

        #request word sequence
        self.request = self.req_obj.get('request', '')

        #request received from (julius, jabber any other resources)
        self.req_from = self.req_obj.get('from', '')

        self.response = ''

    @classmethod
    def run(self):
        """default method"""

        #start sqlalchemy session

        sess = Session()

        sender = self.req_obj.get('sender', '')

        #exctract sender email
        email = sender.split('/')[0]

        #find user profile by primary email
        profile = sess.query(Profile).filter(Profile.email == email).one()

        if profile:
            pass

        response = 'sorry you are not allowed to tweet'
        if profile.type == 'admin' and self.req_from == 'jabber':
            response = tweet(" ".join(self.args))
            response = 'Done. Check it at http://twitter.com/myname'

        if self.req_from == 'jabber':
            todo = {'text': response, 'jmsg': response, 'type': 'response'}
            self.response = todo

        if self.req_from == 'julius':
            bang()
            todo = {'say': response, 'text': response, 'type': 'response'}
            self.response = say(self.request.replace('say', '').upper())

        return self.response

#direct test
#r = Reaction(**{'req_obj':{'request': '', 'from' : '','sender': 'your.name@gmail.com' }})
#r.run()
