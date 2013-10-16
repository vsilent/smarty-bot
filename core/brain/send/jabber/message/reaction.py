#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Author:
Description:
'''
from core.broadcast import say, bang
from core.config.settings import logger
from core.config import settings
from core.lib.jabber.send_msg import SendMsgBot
from core.people.person import Profile, Session


class Reaction:
    """class Reaction"""
    response = ''
    request = ''

    def __str__(self):
        return 'Send message via jabber'

    @classmethod
    def __init__(self, *args, **kwargs):
        """ original request string """
        #logger.info(args)
        #logger.info(kwargs)
        logger.info(kwargs.get('req_obj'))

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

        email = None
        sender = self.req_obj.get('sender', '')

        if sender:
            email = sender.split('/')[0]

        sess = Session()
        #exctract uuid
        uuid = self.req_obj.pop('uuid', '')
        msg = self.request.replace('send jabber message', '')

        if email:
            #find user profile by primary email
            profile = sess.query(Profile).filter(Profile.email == email).one()
        elif uuid:
            #find user profile by uuid
            profile = sess.query(Profile).filter(Profile.uuid == uuid).one()
        else:
            response = 'You are not allowed to send message'
            todo = {'text': response,
                    'jmsg': response,
                    'type': 'response'}
            self.response = todo
            return self.response

        if profile.type == 'admin' and self.req_from == 'jabber':
            logger.info('Sending message..')
            profiles = sess.query(Profile).all()
            for p in profiles:
                xmpp = SendMsgBot(
                    settings.MY_ACCOUNTS['gmail']['email'],
                    settings.MY_ACCOUNTS['gmail']['password'],
                    p.email, msg)

                # Connect to the XMPP server
                # and start processing XMPP stanzas.
                if xmpp.connect():
                    xmpp.process(threaded=False)
                    logger.info("Done")
                else:
                    logger.info("Unable to connect.")

            response = 'Message sent.'
        else:
            response = 'You are not allowed to send broadcast messages.'

        #########################################
        # If executed by jabber client          #
        #########################################
        if self.req_from == 'jabber':
            todo = {'text': response, 'jmsg': response, 'type': 'response'}
            self.response = todo

        #########################################
        # If executed by crontab                #
        #########################################

        if self.req_from == 'cron':
            todo = {'text': response, 'jmsg': response, 'type': 'response'}
            response = self.req_obj.get('cmd_args', '')
            logger.info('Sending cron notification to user.')
            xmpp = SendMsgBot(
                settings.MY_ACCOUNTS['gmail']['email'],
                settings.MY_ACCOUNTS['gmail']['password'],
                profile.email, response)

            # Connect to the XMPP server and start processing XMPP stanzas.
            if xmpp.connect():
                xmpp.process(threaded=False)
                logger.info("Done")
            else:
                logger.info("Unable to connect.")

            xmpp.disconnect()
            self.response = todo

        #########################################
        # If executed by julius client          #
        #########################################

        if self.req_from == 'julius':
            bang()
            todo = {'say': response, 'text': response, 'type': 'response'}
            self.response = say(self.request.replace('say', '').upper())

        return self.response


##n = Reaction(*{'reserved':''}, **{'req_obj':{'from':'', 'request':''}})
##n.run()

#if self.req_from == 'jabber':
#todo = { 'text' : response, 'jmsg' : response, 'type': 'response' }
#self.response = todo

#if self.req_from == 'julius':
#bang()
#todo = { 'say': response , 'text' : response ,'type': 'response' }
#self.response = say(self.request.replace('say', '').upper())

#return self.response
