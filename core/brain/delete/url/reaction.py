#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Author:
Description:
'''
from core.broadcast import say, bang
from core.config.settings import logger
from core.people.person import Profile
from core.people.person import ProfileLink
from core.people.person import Session
from sqlalchemy import and_
from sqlalchemy.orm.exc import NoResultFound


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
        profile = sess.query(Profile).filter(
            Profile.email == email).one()

        #exstract url from request
        url = self.request.replace('delete url ', '', 1)

        # should be replaced later with one line now it's a kinda shit
        url = url.replace('delete link ', '', 1)
        url = url.replace('delete site ', '', 1).strip()
        url = url.replace('remove link ', '', 1)
        url = url.replace('remove site ', '', 1).strip()
        url = url.replace('remove url ', '', 1).strip()

        #if url.startswith(('http', 'https')):
            #pass

        response = ''
        existing = None

        if url:
            try:
                existing = sess.query(
                    ProfileLink).filter(and_(
                        ProfileLink.url == url,
                        ProfileLink.uuid == profile.uuid)).one()
            except NoResultFound:
                response = "Could not find %s in your list\n" % url
                hs = sess.query(ProfileLink).filter(
                    ProfileLink.uuid == profile.uuid).all()
                hosts = [h.url for h in hs]
                logger.info(hosts)
                response += "\n".join(hosts)
                response += "\nPlease check syntax and try again"
            except Exception as e:
                logger.exception(e)

            if existing:
                sess.delete(existing)
                try:
                    sess.query(ProfileLink).filter(
                        and_(
                            ProfileLink.url == url,
                            ProfileLink.uuid == profile.uuid
                        )
                    ).one()
                except NoResultFound:
                    response = 'Ok. Deleted.'
                else:
                    response = "Could not remove %s \n" % existing.url
                    hs = sess.query(ProfileLink).filter(
                        ProfileLink.uuid == profile.uuid).all()
                    hosts = [h.url for h in hs]
                    logger.info(hosts)
                    response += "\n".join(hosts)
                    response += "\nPlease try again"

        if self.req_from == 'jabber':
            todo = {'text': response,
                    'jmsg': response,
                    'type': 'response'}
            self.response = todo

        elif self.req_from == 'julius':
            bang()
            todo = {'say': response,
                    'text': response,
                    'type': 'response'}
            self.response = say(self.request.replace('say', '').upper())

        return self.response
