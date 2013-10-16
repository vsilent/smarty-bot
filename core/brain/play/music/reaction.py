#!/usr/bin/env python
# -*- coding: utf-8 -*-

from core.config.settings import DEMO_MUSIC_DIR, PLAYER_PATH, logger
import subprocess
import os, random

class Reaction:
    """class Reaction"""
    request  = ''
    response = ''
    pid = False

    def __str__(self):
        return 'Play music reaction (random)'

    @classmethod
    def __init__(self, *args, **kwargs):
        """ original request string """
        #logger.info(args)
        #logger.info(kwargs)
        #logger.info(kwargs.get('req_obj'))
        self.request = kwargs.pop('req_obj')['request']
        self.response = ''

    @classmethod
    def continue_dialog(self):
        """ False will stop current dialog after this reaction and start new from begining
            otherwise will continue to store request
        """
        return True

    @classmethod
    def run(self):
        """default method"""
        _file = DEMO_MUSIC_DIR + random.choice( os.listdir( DEMO_MUSIC_DIR ) )
        logger.info('Playing... %s ' % _file )
        proc = subprocess.Popen( [ "%s" % PLAYER_PATH, _file ] )
        return self.response
