#!/usr/bin/env python
'''
Author:
Description:
'''
from core.broadcast import say, bang
from core.config.settings import logger
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

        sender = self.req_obj.get('sender', '')
        email = sender.split('/')[0]
        sess = Session()
        profile = None

        try:
            profile = sess.query(Profile).filter(Profile.email == email).one()
        except Exception, e:
            logger.exception(e)

        logger.info('%s' % self.request)

        req = self.request.strip().replace('my zip is ', '')
        try:
            profile.home_postcode = req
            sess.add(profile)
            sess.commit()

        except Exception as e:
            logger.exception(e)

        response = 'ok %s, your zip code is %s' % (profile.first_name, req)

        if self.req_from == 'jabber':
            todo = {'text': response, 'jmsg': response, 'type': 'response'}
            self.response = todo

        if self.req_from == 'julius':
            bang()
            todo = {'say': response, 'text': response, 'type': 'response'}
            self.response = say(self.request.replace('say', '').upper())

        return self.response
