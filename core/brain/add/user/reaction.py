#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Author:
Description:
'''
from core.broadcast import say, bang
from core.config.settings import logger
from core.people.person import Profile, Session, add_profile
from sqlalchemy import and_


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
        req = self.request.replace('add user', '', 1)
        name = req.strip().split()

        response = 'sorry you are not allowed to add new users'
        if profile.type == 'admin' and self.req_from == 'jabber':
            if name:
                logger.info('new user %s' % name)
                exists = sess.query(Profile).filter(
                    and_(Profile.first_name == name[0],
                         Profile.last_name == name[1])).all()
                user = {}

                if not exists:
                    try:
                        user['first_name'] = name[0]
                        user['last_name'] = name[1]
                        user['email'] = name[2]
                        add_profile(user)

                    except Exception as e:
                        sess.rollback()
                        logger.exception(e)

                    response = '%s added' % name
                else:
                    response = 'looks like %s is already exists' % name

            else:
                response = """
                Hmm  could not parse name,
                can you add it like this:
                    add user John Smith john.smith@gmail.com"""

        if self.req_from == 'jabber':
            todo = {'text': response, 'jmsg': response, 'type': 'response'}
            self.response = todo

        if self.req_from == 'julius':
            bang()
            todo = {'say': response, 'text': response, 'type': 'response'}
            self.response = say(self.request.replace('say', '').upper())

        return self.response
