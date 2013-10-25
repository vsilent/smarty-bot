#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Author:
Description:
'''
from core.broadcast import say, bang
from core.config.settings import logger
from core.people.person import Profile, ProfileLink, Session
from sqlalchemy import and_
import re


class Reaction:
    """class Reaction"""
    response = ''
    request = ''

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

        #start sqlalchemy session
        sess = Session()

        sender = self.req_obj.get('sender', '')

        #exctract sender email
        email = sender.split('/')[0]

        #find user profile by primary email
        profile = sess.query(Profile).filter(Profile.email == email).one()

        #exstract url from request
        req = self.request.replace('add url', '', 1).strip()

        # should be replaced later with one replacement
        req = self.request.replace('add link ', '', 1)
        req = self.request.replace('add site ', '', 1)

        url = re.search("(?P<url>https?://[^\s]+)", req).group("url")
        logger.info('got %s' % url)

        if url:
            exists = sess.query(ProfileLink).filter(
                and_(ProfileLink.url == url, ProfileLink.uuid == profile.uuid)
            ).all()
            link = {}

            if not exists:
                try:
                    link['url'] = url
                    link['type'] = 'external'
                    link['uuid'] = profile.uuid

                    l = ProfileLink(**link)
                    sess.add(l)
                    sess.commit()

                except Exception as e:
                    sess.rollback()
                    logger.exception(e)

                response = '%s added to your collection' % url
            else:
                response = 'looks like %s is already in collection' % url

        else:
            response = 'seems like %s is not valid url' % url

        if self.req_from == 'jabber':
            todo = {
                'text': response,
                'jmsg': response,
                'type': 'response'
            }
            self.response = todo

        if self.req_from == 'julius':
            bang()
            todo = {
                'say': response,
                'text': response,
                'type': 'response'
            }
            self.response = say(self.request.replace('say', '').upper())

        return self.response

#direct test
#r = Reaction(**{'req_obj':{
#'request': '', 'from' : '','sender': 'your.name@gmail.com' }})
#r.run()
