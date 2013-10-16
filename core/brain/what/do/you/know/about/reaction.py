#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Author:
Description:
'''
from core.broadcast import say, bang
from core.config.settings import logger
from core.people.person import *

class Reaction:
    """class Reaction"""
    response = ''
    request  = ''

    def __str__(self):
        return 'My new reaction'

    @classmethod
    def __init__(self, *args, **kwargs):
        """ original request string """
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

        name = req.strip().split()

        full_profile = sess.query( Profile ) \
                .outerjoin( ProfileEmail, ProfileEmail.uuid == Profile.uuid) \
        .outerjoin( ProfilePhone, ProfilePhone.uuid == Profile.uuid) \
        .outerjoin( ProfileSocial, ProfileSocial.uuid == Profile.uuid) \
        .outerjoin( ProfileInterest, ProfileInterest.uuid == Profile.uuid) \
        .outerjoin( ProfileOtherName, ProfileOtherName.uuid == Profile.uuid) \
        .filter_by(Profile.first_name.like(name[0]), Profile.last_name.like(name[1])).one()
        #.outerjoin( ProfileDevice, ProfileDevice.uuid == Profile.uuid) \
        #.outerjoin( ProfilePicture, ProfilePicture.uuid == Profile.uuid) \
        #.outerjoin( ProfileRequest, ProfileRequest.uuid == Profile.uuid) \
        #.outerjoin( ProfileComment, ProfileComment.uuid == Profile.uuid) \
        #.outerjoin( ProfileRelation, ProfileRelation.uuid == Profile.uuid) \
        #.outerjoin( ProfileCronjob, ProfileCronjob.uuid == Profile.uuid) \

        #logger.info('%s' % full_profile)
        #logger.info('%s' % full_profile.uuid)
        #logger.info('%s' % full_profile.first_name)

        if full_profile:
            response = 'You are %s %s with primary e-mail: %s ' % ( full_profile.first_name, full_profile.last_name, full_profile.email )
        elif profile:
            response = 'You are %s %s with primary e-mail: %s' % ( profile.first_name, profile.last_name, profile.email )
        else:
            response = ''

        if self.req_from == 'jabber':
            todo = { 'text' : response, 'jmsg' : response, 'type': 'response' }
            self.response = todo

        if self.req_from == 'julius':
            bang()
            todo = { 'say': response , 'text' : response ,'type': 'response' }
            self.response = say(self.request.replace('say', '').upper())

        return self.response

