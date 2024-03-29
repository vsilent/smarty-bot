#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Description: register hours

'''
from core.people.person import Profile, Session, ProfileTimesheet
from core.utils.sys.report import report_bug
from config.settings import logger
import datetime
#import zmq


class Reaction:
    """Update my details reaction"""
    response = ''
    request = ''
    xmpp = ''

    def __str__(self):
        return 'Begin update my deatils'

    @classmethod
    def __init__(self, *args, **kwargs):
        """ original request string """
        #get request object
        self.req_obj = kwargs.get('req_obj')

        #request word sequence
        self.request = self.req_obj.get('request', '')

        #request received from (julius, jabber any other resources)
        self.req_from = self.req_obj.get('from', '')

        #get command history
        self.cmd_stack = kwargs.pop('cmd_stack', '')

        self.response = ''


    @classmethod
    def run(self):
        """default method"""

        logger.debug(self.req_obj)
        uuid = self.req_obj.get('uuid', '')
        sender = self.req_obj.get('sender', '')
        sess = Session()

        self.response = {
            'text': "I couldn't find your profile by %s" % uuid,
            'jmsg': "I couldn't find your profile by %s" % uuid,
            'type': 'response'}

        #########################################
        # check and get profile                 #
        #########################################

        if uuid:
            try:
                profile = sess.query(Profile).filter(
                    Profile.uuid == uuid).one()
            except Exception as e:
                logger.exception(e)
                return self.response

        if sender:
            #exctract sender email
            email = sender.split('/')[0]

            try:
                profile = sess.query(
                    Profile).filter(
                        Profile.email == email).one()
            except Exception as e:
                logger.exception(e)
                return self.response

        ask = [property for prop in profile if not prop]:
        sys.exit()


        request_to_user = 'Ok, what is your %s ?' % profile.first_name

        todo = {'request': request_to_user,
                'from': 'jabber',
                'type': 'response',
                'continue': 1,
                'text': request_to_user,
                'jmsg': request_to_user,
                'sender': str(profile.email)}

        #########################################
        # If executed by crontab                #
        #########################################

        if self.req_from == 'cron':
            #args = self.req_obj.get('cmd_args', '')
            logger.info('Sending cron notification to user.')
            #logger.info('Trying to connect jabber socket and send a message.')
            #context = zmq.Context()
            #sock = context.socket(zmq.REQ)
            #sock.connect('ipc:///tmp/smarty-jabber')
            #sock.send_json({'request': request_to_user,
                            #'from': 'jabber',
                            #'type': 'response',
                            #'continue': 1,
                            #'sender': str(profile.email)})
            #res_obj = sock.recv_json()
            #logger.info('======================= response obj ========================')
            #logger.debug(res_obj)
            #self.xmpp.Message(profile.email, request_to_user)
            #self.response = res_obj

        if self.req_from == 'jabber':
            self.response = todo

        if self.req_from == 'julius':
            from core.broadcast import say, bang
            bang()
            todo['type'] = 'response'
            todo['say'] = request_to_user
            self.response = say(self.request.replace('say', '').upper())

        return self.response

    @classmethod
    def on_continue(self, msg):
        """docstring for on_continue"""
        todo = {}
        response = "Ok."
        request = msg.get('request', None)
        sender = msg.get('sender', '')
        req_from = msg.get('from', '')
        #error = msg.get('error', '')
        #logger.info('error %s..........................' % error)
        #logger.info('req_from %s..........................' % req_from)
        #logger.info('request %s..........................' % request)

        sess = Session()

        #exctract sender email
        email = sender.split('/')[0]

        #find user profile by primary email
        profile = sess.query(Profile).filter(Profile.email == email).one()

        if self.is_correct_format(request):
            insert = {}
            insert['uuid'] = profile.uuid
            insert['type'] = 'custom'
            insert['created'] = datetime.datetime.utcnow()
            logger.debug('request type %s' % type(request), request)
            insert['spent'] = request

            try:
                ts = ProfileTimesheet(**insert)
                sess.add(ts)
                sess.commit()
            except Exception as e:
                sess.rollback()
                logger.exception(e)
                report_bug(e)
                response = 'I could not save it, problem has \
                been already reported to developer'
        else:
            response = " type something like:  8 hours "
            todo['continue'] = 1

        if req_from == 'jabber':
            todo = {'text': response,
                    'jmsg': response,
                    'type': 'response',
                    'continue': 0}
            self.response = todo

        if req_from == 'julius':
            from core.broadcast import say, bang
            bang()
            todo = {'say': response,
                    'text': response,
                    'type': 'response',
                    'continue': 0}
            self.response = say(self.request.replace('say', '').upper())

        return self.response

    @classmethod
    def is_correct_format(self, request):
        """later will parse for correct format """
        return request
