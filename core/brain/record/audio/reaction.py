#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Author:
Description:
'''
import subprocess
import logging
from core.config.settings import APP_DIRS


class Reaction:

    @classmethod
    def __str__(self):
        """ """
        return 'This class provides .... '

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
    def continue_dialog(self):
        return True

    #this method will be executed by default
    @classmethod
    def run(self):
        p1 = subprocess.Popen(
            ['arecord', "-f", "cd", "-t", "raw"], stdout=subprocess.PIPE
        )

        command = ['oggenc', '-', '-r', '-o',
                   '%srecording.ogg' % APP_DIRS['tmp_input_audio_dir']]

        logging.info("write to %s ", command)

        p2 = subprocess.Popen(
            command,
            stdin=p1.stdout,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        logging.info('Start audio recording...')
        output, err = p2.communicate()
        logging.info("%s", err)
        return True
