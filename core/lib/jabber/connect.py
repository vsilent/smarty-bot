#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" jabber  """
import sys
import sleekxmpp
import zmq

from core.config import settings
from core.config.settings import logger
from core.people import person
from core.config.settings import REDIS
import redis

import atexit

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


class SendSubscriptionBot(sleekxmpp.ClientXMPP):
    """
    A basic SleekXMPP bot that will log in, send a subscription,
    and then log out.
    """
    pfrom = None
    msg = None

    def __init__(self, jid, password, recipient):
        sleekxmpp.ClientXMPP.__init__(self, jid, password)
        self.pfrom = jid
        self.recipient = recipient
        self.add_event_handler("session_start", self.start)

    def start(self, event):
        self.send_presence_subscription(
            pfrom=self.pfrom, pto=self.recipient
        )
        self.disconnect(wait=True)
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
    nick = settings.MY_NAME
    _redis = None
    context = None
    """
    A simple SleekXMPP bot that will echo messages it
    receives, along with a short thank you message.
    """
    def __init__(self, jid, password):
        sleekxmpp.ClientXMPP.__init__(self, jid, password)

        self.auto_subscribe = True
        self.auto_authorize = True
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
        self.add_event_handler("presence_available", self.presence_available)
        self.add_event_handler("groupchat_presence", self.muc_presence)
        self.add_event_handler("groupchat_message", self.muc_message)
        self.add_event_handler("groupchat_invite", self.accept_invite)
        self.add_event_handler(
            "groupchat_direct_invite",
            self.accept_direct_invite
        )

        self._redis = redis.Redis(
            host=REDIS['host'],
            # password=REDIS['password'],
            # unix_socket_path=REDIS['socket']
        )

        # send and listen commands
        self.context = zmq.Context()
        self.sock = self.context.socket(zmq.REQ)
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

        #self._start_thread("chat_send", self.chat_send)

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

        if msg['from'] != self.nick and msg['type'] != 'groupchat' and len(msg['body'].strip()) != 0:
            pass
            # logger.info("received: %s from %s of type %s resource %s",
                        # msg['body'],
                        # msg['from'],
                        # msg['type'],
                        # self.resource)

        #temporary
        person.update_list_from_jabber(
            self.roster[settings.MY_ACCOUNTS['gmail']['email']]
        )

        self.sock.send_json({
            'request': msg['body'],
                         'from': SERVICE_NAME,
                         'type': 'request',
            'sender': str(msg['from'])
        })

        res_obj = self.sock.recv_json()
        if isinstance(res_obj, dict):
            # any string (the plain text message body)
            msg['body'] = res_obj['text']
            msg.reply("%(body)s" % msg).send()

    def presence_available(self, iq):
        logger.info(">>>>>> chat presence, here is iq %s", iq)
        person.update_list_from_jabber(
            self.roster[settings.MY_ACCOUNTS['gmail']['email']]
        )
        #logger.info("here we are 1 chat room %s", iq)
# this should be a request for read info from spinbackup
        #self.outsock.send_json({'cmd': 'get_news'})
        #msg = self.outsock.recv_json()
        #if msg:
            #logger.info("twitter bot tryes to send message to chat room %s", iq)
            #self.send_message(
                ## self.nick
                ##mto=msg['from'].bare,
                #mto='',
                #mbody=msg['text'],
                #mtype='groupchat'
            #)

    def muc_presence(self, iq):
        """docstring for groupchat_presence"""

        #logger.info(">>>>>> groupchat presence worked, here we are in chat room %s", iq)
        key = 'twitter_hourly'
        msg = self._redis.get(key)
        if msg:
            self._redis.delete(key)
            logger.info("twitter bot tryes to send message to chat room %s", iq)
            self.send_message(
                # self.nick
                mto=iq['from'].bare,
                mbody=msg,
                mtype='groupchat'
            )
            msg = None

    #def chat_send(self):
        #while True:
            #msg = self.outsock.recv_json()
            #if msg:
                #self.send_message(
                    ## self.nick
                    #mto=msg['from'].bare,
                    #mbody=msg['text'],
                    #mtype='groupchat'
                #)

    def muc_message(self, msg):
        """
        Process incoming message stanzas from any chat room. Be aware
        that if you also have any handlers for the 'message' event,
        message stanzas may be processed by both handlers, so check
        the 'type' attribute when using a 'message' event handler.

        Whenever the bot's nickname is mentioned, respond to
        the message.

        IMPORTANT: Always check that a message is not from yourself,
                   otherwise you will create an infinite loop responding
                   to your own messages.

        This handler will reply to messages that mention
        the bot's nickname.

        Arguments:
            msg -- The received message stanza. See the documentation
                   for stanza objects and the Message stanza to see
                   how it may be used.
        """
        if msg['mucnick'] not in (self.nick, self.nick.lower()) and\
                self.nick in msg['body'] and msg['type'] == 'groupchat':
            """self.send_message(mto=msg['from'].bare,
            #mbody="I heard that, %s." % msg['mucnick'],
            #mtype='groupchat')
            """
            #  cut nickname
            if msg['body'].startswith(self.nick.lower()):
                mesg = msg['body'].replace(self.nick.lower(), '', 1)

            if msg['body'].startswith(self.nick):
                mesg = msg['body'].replace(self.nick, '', 1)

            if mesg.startswith(','):
                mesg = mesg.replace(',', '', 1)

            self.sock.send_json({
                'request': mesg,
                'from': SERVICE_NAME,
                'type': 'request',
                'sender': str(msg['from'])
            })

            res_obj = self.sock.recv_json()
            if not res_obj:
                self.send_message(
                    mto=msg['from'].bare,
                    mbody='one moment please..',
                    mtype='groupchat'
                )
            if res_obj:
                self.send_message(
                    mto=msg['from'].bare,
                    mbody=res_obj['text'],
                    mtype='groupchat'
                )

        key = 'twitter_hourly'
        tmsg = self._redis.get(key)
        self._redis.delete(key)
        if tmsg:
            self.send_message(
                mto=msg['from'].bare,
                mbody=tmsg,
                mtype='groupchat'
            )

    def muc_online(self, presence):
        """
        Process a presence stanza from a chat room. In this case,
        presences from users that have just come online are
        handled by sending a welcome message that includes
        the user's nickname and role in the room.

        Arguments:
            presence -- The received presence stanza. See the
                        documentation for the Presence stanza
                        to see how else it may be used.
        """
        if presence['muc']['nick'] != self.nick:
            self.send_message(mto=presence['from'].bare,
                              mbody="Hello, %s %s" % (presence['muc']['role'],
                                                      presence['muc']['nick']),
                              mtype='groupchat')

    def accept_invite(self, inv):
        self.plugin['xep_0045'].joinMUC(inv["from"], self.nick, wait=False)

    def accept_direct_invite(self, inv):
        self.plugin['xep_0045'].joinMUC(inv["from"], self.nick, wait=False)

if __name__ == '__main__':
    # Setup the EchoBot and register plugins. Note that while plugins may
    # have interdependencies, the order in which you register them does
    # not matter.

    xmpp = EchoBot(settings.MY_ACCOUNTS['gmail']['email'],
                   settings.MY_ACCOUNTS['gmail']['password'])

    xmpp.auto_subscribe = True
    xmpp.auto_authorize = True
    xmpp.register_plugin('xep_0030')  # Service Discovery
    xmpp.register_plugin('xep_0045')  # Multi-User Chat
    xmpp.register_plugin('xep_0249')  # XEP-0249: Direct MUC Invitations
    xmpp.register_plugin('xep_0199')  # XMPP Ping
    xmpp.register_plugin('xep_0004')  # Data Forms
    xmpp.register_plugin('xep_0060')  # PubSub

    @atexit.register
    def goodbye():
        xmpp.sock.close()
        xmpp.context.term()

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
