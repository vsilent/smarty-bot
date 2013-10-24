#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" jabber  """
#import os
import sys
#import time
import sleekxmpp
import zmq

from core.config import settings
from core.config.settings import logger
from core.people import person
#from multiprocessing import Process, Pipe


"""
    SleekXMPP: The Sleek XMPP Library
    Copyright (C) 2010  Nathanael C. Fritz
    This file is part of SleekXMPP.

    See the file LICENSE for copying permission.
"""

SERVICE_NAME = 'jabber'

# Python versions before 3.0 do not use UTF-8 encoding
# by default. To ensure that Unicode is handled properly
# throughout SleekXMPP, we will set the default encoding
# ourselves to UTF-8.
if sys.version_info < (3, 0):
    reload(sys)
    sys.setdefaultencoding('utf8')
else:
    raw_input = input


class SendMsgBot(sleekxmpp.ClientXMPP):

    """
    A basic SleekXMPP bot that will log in, send a message,
    and then log out.
    """

    def __init__(self, jid, password, recipient, message):
        sleekxmpp.ClientXMPP.__init__(self, jid, password)

        # The message we wish to send, and the JID that
        # will receive it.
        self.recipient = recipient
        self.msg = message

        # The session_start event will be triggered when
        # the bot establishes its connection with the server
        # and the XML streams are ready for use. We want to
        # listen for this event so that we we can intialize
        # our roster.
        self.add_event_handler("session_start", self.start)

    def start(self, event):
        """
        Process the session_start event.

        Typical actions for the session_start event are
        requesting the roster and broadcasting an intial
        presence stanza.

        Arguments:
            event -- An empty dictionary. The session_start
                     event does not provide any additional
                     data.
        """
        self.send_presence()
        self.get_roster()

        self.send_message(mto=self.recipient,
                          mbody=self.msg,
                          mtype='chat')

        # Using wait=True ensures that the send queue will be
        # emptied before ending the session.
        self.disconnect(wait=True)


class EchoBot(sleekxmpp.ClientXMPP):

    sock = None
    """
    A simple SleekXMPP bot that will echo messages it
    receives, along with a short thank you message.
    """
    def __init__(self, jid, password):
        sleekxmpp.ClientXMPP.__init__(self, jid, password)

        # The session_start event will be triggered when
        # the bot establishes its connection with the server
        # and the XML streams are ready for use. We want to
        # listen for this event so that we we can intialize
        # our roster.
        self.add_event_handler("session_start", self.start)

        # The message event is triggered whenever a message
        # stanza is received. Be aware that that includes
        # MUC messages and error messages.
        self.add_event_handler("message", self.message)
        self.add_event_handler("presence_available", self.presense_available)

        context = zmq.Context()
        self.sock = context.socket(zmq.REQ)
        #self.sock.bind('ipc:///tmp/smarty-jabber')
        self.sock.connect('ipc:///tmp/smarty-jabber')

    def start(self, event):
        """
        Process the session_start event.

        Typical actions for the session_start event are
        requesting the roster and broadcasting an intial
        presence stanza.

        Arguments:
            event -- An empty dictionary. The session_start
                     event does not provide any additional
                     data.
        """
        self.send_presence()
        self.get_roster()

        person.update_list_from_jabber(
            self.roster[settings.MY_ACCOUNTS['gmail']['email']]
        )

    def message(self, msg):
        """
        Process incoming message stanzas. Be aware that this also
        includes MUC messages and error messages. It is usually
        a good idea to check the messages's type before processing
        or sending replies.

        Arguments:
            msg -- The received message stanza. See the documentation
                   for stanza objects and the Message stanza to see
                   how it may be used.
        """

        logger.info("received: %s from %s of type %s resource %s",
                    msg['body'],
                    msg['from'],
                    msg['type'],
                    self.resource)

        #temporary
        person.update_list_from_jabber(
            self.roster[settings.MY_ACCOUNTS['gmail']['email']]
        )

        self.sock.send_json({'request': msg['body'],
                             'from': SERVICE_NAME,
                             'type': 'request',
                             'sender': str(msg['from'])})

        res_obj = self.sock.recv_json()
        # any string (the plain text message body)
        msg['body'] = res_obj['text']
        msg.reply("%(body)s" % msg).send()

    def presense_available(self, iq):
        """docstring for presense_available"""
        #logger.info('we are here in my handler')
        #logger.info(type(iq))
        #self.send_message(mto=self.recipient,
        #mbody=self.msg,
        #mtype='chat')
        #pass

if __name__ == '__main__':
    # Setup the EchoBot and register plugins. Note that while plugins may
    # have interdependencies, the order in which you register them does
    # not matter.
    #send message
    #to = 'jabberroid@gmail.com'
    #message = 'Im ready'
    #xmpp_send = SendMsgBot(settings.MY_ACCOUNTS['gmail']['email'],
                           #settings.MY_ACCOUNTS['gmail']['password'],
                           #to,
                           #message)
    # Setup the MUCBot and register plugins. Note that while plugins may
    # have interdependencies, the order in which you register them does
    # not matter.
    #room = ''
    #nick = settings.MY_NAME
    #xmpp = MUCBot(settings.MY_ACCOUNTS['gmail']['email'],
    #settings.MY_ACCOUNTS['gmail']['password'], room, nick)

    xmpp = EchoBot(settings.MY_ACCOUNTS['gmail']['email'],
                   settings.MY_ACCOUNTS['gmail']['password'])

    xmpp.register_plugin('xep_0030')  # Service Discovery
    xmpp.register_plugin('xep_0045')  # Multi-User Chat
    xmpp.register_plugin('xep_0199')  # XMPP Ping
    xmpp.register_plugin('xep_0004')  # Data Forms
    xmpp.register_plugin('xep_0060')  # PubSub

    # Connect to the XMPP server and start processing XMPP stanzas.
    if xmpp.connect():
        # If you do not have the pydns library installed, you will need
        # to manually specify the name of the server if it does not match
        # the one in the JID. For example, to use Google Talk you would
        # need to use:
        #
        # if xmpp.connect(('talk.google.com', 5222)):
        #     ...
        xmpp.process(threaded=False)
        #logger.info("Done")
    else:
        logger.info("Unable to connect")

    # If you are working with an OpenFire server, you may need
    # to adjust the SSL version used:
    # xmpp.ssl_version = ssl.PROTOCOL_SSLv3

    # If you want to verify the SSL certificates offered by a server:
    # xmpp.ca_certs = "path/to/ca/cert"

    # Connect to the XMPP server and start processing XMPP stanzas.
    if xmpp.connect():
        # If you do not have the pydns library installed, you will need
        # to manually specify the name of the server if it does not match
        # the one in the JID. For example, to use Google Talk you would
        # need to use:
        #
        # if xmpp.connect(('talk.google.com', 5222)):
        #     ...
        xmpp.process(threaded=False)
    else:
        logger.error("Unable to connect")
