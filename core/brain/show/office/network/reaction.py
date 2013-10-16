#!/usr/bin/env python
# -*- coding: utf-8 -*-

import nmap                         # import nmap.py module
from core.broadcast import say, bang
from core.config.settings import logger
from core.config import settings
from core.lib.jabber.send_msg import SendMsgBot
from core.people.person import Profile, Session



class Reaction:
    """class Reaction"""
    response = ''
    request  = ''

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

        response = 'Sorry, you are not allowed to do that.'

        if email:
            #find user profile by primary email
            profile = sess.query(Profile).filter(Profile.email == email).one()
        elif uuid:
            #find user profile by uuid
            profile = sess.query(Profile).filter(Profile.uuid == uuid).one()
        else:
            todo = { 'text' : response, 'jmsg' : response, 'type': 'response' }
            self.response = todo
            return self.response

        if profile.type  == 'admin' and self.req_from == 'jabber':
            nm = nmap.PortScanner()                             # instantiate nmap.PortScanner object
            nm.scan(hosts='192.168.1.0/24', arguments='-sP')
            nm.command_line()                                   # get command line used for the scan : nmap -oX - -p 22-443 127.0.0.1
            nm.scaninfo()                                       # get nmap scan informations {'tcp': {'services': '22-443', 'method': 'connect'}}
            hosts_list = [(x, nm[x]['status']['state'], nm[x]['hostname']) for x in nm.all_hosts()]
            #for host, status, name in hosts_list:
                #print('{0}:{1}:{2}'.format(host, status, name))
            response = hosts_list


        #########################################
        # If executed by jabber client          #
        #########################################

        if self.req_from == 'jabber':
            todo = { 'text' : response, 'jmsg' : response, 'type': 'response' }
            self.response = todo

        if self.req_from == 'julius':
            response = 'see information in the log file'
            todo = { 'text' : response, 'jmsg' : response, 'type': 'response' }
            self.response = todo

        return self.response
