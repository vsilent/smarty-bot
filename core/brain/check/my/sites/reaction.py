#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Author:
Description:
'''
from core.broadcast import say, bang
from core.config.settings import logger
from core.people.person import Profile, ProfileLink, Session
from core.utils.network.email import send
from core.config import settings
import urllib2


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
        hosts = None
        profile = None
        response = ''

        #exctract sender email
        if sender:
            email = sender.split('/')[0]
            #find user profile by primary email
            profile = sess.query(Profile).filter(
                Profile.email == email).one()

        if uuid:
            #find user profile by uuid
            profile = sess.query(Profile).filter(
                Profile.uuid == uuid).one()

        if profile:
            hosts = sess.query(ProfileLink).filter(
                ProfileLink.uuid == profile.uuid).all()

        code = -1
        if hosts:
            for h in hosts:
                logger.info('open http connection to %s ..' % h.url)
                try:
                    r = urllib2.urlopen(h.url)
                    code = r.code
                except Exception:
                    code = -1
                    #logger.exception(e)

                if code != 200:
                    response += "Could not connect %s \n" % (h.url)
        else:
            response = 'you have no urls that I can check, ' + \
                'add url by command: add url http://mysite.com'

        if self.req_from == 'jabber':
            if response == '':
                response  = 'looks like everything is ok.'
            todo = {'text': response, 'jmsg': response, 'type': 'response'}
            self.response = todo
        elif self.req_from == 'julius':
            bang()
            todo = {'say': response, 'text': response, 'type': 'response'}
            self.response = say(self.request.replace('say', '').upper())
        elif response:
            send(settings.MY_ACCOUNTS['gmail']['email'],
                 profile.email,
                 'check my sites report from Smarty',
                 response)
            todo = {'text': response, 'jmsg': response, 'type': 'response'}
            self.response = todo

        return self.response
