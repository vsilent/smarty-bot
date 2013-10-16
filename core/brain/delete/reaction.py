#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Author:
Description:
'''
from core.broadcast import say, bang
#from core.config.settings import logger
from core.people.person import Profile
from core.people.person import ProfileLink
from core.people.person import Session
from sqlalchemy import and_
import re


class Reaction:
    """Reaction that should recognize what client wants
    to remove and should pass control to another reaction"""
    request = ''
    response = ''

    def __str__(self):
        return 'My new reaction'

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
    def run(self):
        """default method"""

        response = ''
        #start sqlalchemy session
        sess = Session()

        sender = self.req_obj.get('sender', '')

        #exctract sender email
        email = sender.split('/')[0]

        #find user profile by primary email
        profile = sess.query(Profile).filter(Profile.email == email).one()

        #exstract url from request
        url = re.search("(?P<url>https?://[^\s]+)", self.request).group("url")

        if url:
            exists = sess.query(
                ProfileLink).filter(and_(
                    ProfileLink.url == url,
                    ProfileLink.uuid == profile.uuid)).all()
            if exists:
                response = 'Can not remove links yet'
                #pass
                # @todo pass control to delete link
            else:
                response = 'could not find %s' % url

        else:
            #check client's existing data, if request is something else
            pass

        if self.req_from == 'jabber':
            todo = {'text': response,
                    'jmsg': response,
                    'type': 'response'}
            self.response = todo

        if self.req_from == 'julius':
            bang()
            todo = {'say': response,
                    'text': response,
                    'type': 'response'}
            self.response = say(self.request.replace('say', '').upper())

        return self.response
