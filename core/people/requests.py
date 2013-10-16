#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Author:
Description:
'''
from datetime import datetime
from core.config.settings import logger
from core.people.person import Profile, ProfileRequest, Session
from core.config.settings import REDIS
import redis
from core.people.person import update_list_from_jabber


def search_users_request(request, uuid):
        logger.info('Search for a request')

        prefix = 'client-request-'
        response = ''

        #need cache results for an hour because a lot of users
        #can have the same request
        #hour = datetime.now().hour
        minute = datetime.now().minute
        key = prefix + datetime.now().strftime("%Y-%m-%d-") + str(minute)
        old = prefix + datetime.now().strftime("%Y-%m-%d-") + str(minute - 1)

        #use unix socket
        r = redis.Redis(password=REDIS['password'],
                        unix_socket_path=REDIS['socket'])

        existing = r.get(key)

        sess = Session()

        #find user profile by uuid
        profile = sess.query(
            Profile).filter(Profile.uuid == uuid).one()

        #read for all for now
        allowed_for_read = True

        #here I need to know request to be public or not
        if profile.type == 'admin':
            allowed_for_read = True

        if not allowed_for_read:
            return False

        if existing:
            return existing
        else:
            requests = sess.query(ProfileRequest).filter(
                ProfileRequest.request.like('%' + request + '%')).all()
            response = [req.request for req in requests]
            response = "\n".join(response)

            if r.set(key, response):
                r.delete(old)
                return response


def save_users_request(sender, text):
    """ should be in separate file"""
    #start sqlalchemy session
    sess = Session()
    profile = None

    #exctract sender email
    if sender:
        email = sender.split('/')[0]
        if email:
            update_list_from_jabber({email})
            #find user profile by primary email
            profile = sess.query(Profile).filter(
                Profile.email == email).one()

    if not profile:
        return False

    req = {}
    logger.info('save new request %s' % text)
    try:
        req['request'] = text
        req['type'] = 'command'
        req['uuid'] = profile.uuid
        request = ProfileRequest(**req)
        sess.add(request)
        sess.commit()
    except Exception as e:
        sess.rollback()
        logger.exception(e)
