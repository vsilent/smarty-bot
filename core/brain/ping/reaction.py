#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Author:
Description:
'''
from core.broadcast import say, bang
from core.config.settings import logger
from core.utils.network.ping import pinger
from core.people.person import Profile, ProfileLink, Session


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
        sess = Session()
        sender = self.req_obj.get('sender', '')
        uuid = self.req_obj.pop('uuid', '')

        #exctract sender email
        if sender:
            email = sender.split('/')[0]

        if email:
            #find user profile by primary email
            profile = sess.query(Profile).filter(Profile.email == email).one()
        elif uuid:
            #find user profile by uuid
            profile = sess.query(Profile).filter(Profile.uuid == uuid).one()

        #find user profile by primary email
        hs = sess.query(ProfileLink).filter(ProfileLink.uuid == profile.uuid).all()
        hosts = [h.url.replace('https://', '').replace('http://', '') for h in hs]
        logger.info('pinging %s' % hosts)
        response = ''
        at_least_one_host_is_down = False

        if hosts:
            p = pinger()
            p.ping(hosts)
            for h, s in p.response.items():
                if s == 'down':
                    at_least_one_host_is_down = True
                response += "%s is %s \n" % (h, s)
        else:
            response = 'you have to add url by command: add url http://mysite.com'

        if self.req_from == 'jabber':
            todo = {'text': response, 'jmsg': response, 'type': 'response'}
            self.response = todo

        if self.req_from == 'julius':
            bang()
            todo = {'say': response, 'text': response, 'type': 'response'}
            self.response = say(self.request.replace('say', '').upper())

        return self.response
