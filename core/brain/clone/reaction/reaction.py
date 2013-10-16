#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Author:
Description:
'''
from core.people.person import Profile, Session
from core.broadcast import say, bang
from core.utils.utils import Utils
import os
#from core.config.settings import logger


class Reaction:
    """class Reaction"""
    response = ''
    request = ''
    _utils = Utils()

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

        response = 'done.'
        req = self.request.replace('clone reaction ', '', 1).split('to', 1)

        if sender:
            #extract sender email
            email = sender.split('/')[0]
            #find user profile by primary email
            profile = sess.query(Profile).filter(Profile.email == email).one()
            if profile:
                self.create_new_reaction(req)
                old = req[0].strip().replace('\s', '.')
                new = req[1].strip().replace('\s', '.')
                self.replace_import_command(old, new)

        if self.req_from == 'jabber':
            todo = {'text': response, 'jmsg': response, 'type': 'response'}
            self.response = todo

        if self.req_from == 'julius':
            bang()
            todo = {'say': response, 'text': response, 'type': 'response'}
            self.response = say(self.request.replace('say', '').upper())

        return self.response

    @classmethod
    def create_new_reaction(self, text):
        """docstring for create_new_reaction"""
        path = self._utils.get_full_path_to_module_by_request(text)
        #make a copy of default reaction files
        if not os.path.isfile(path + '/reaction.py'):
            self._utils.copy_default_reaction_files(path + '/')

    @classmethod
    def replace_import_command(self, text):
        pass
