#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Author:
Description:
'''
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
        """ False will stop dialog after processing run() method and start new from begining
            otherwise will continue to store request
        """
        return True

    #this method will be executed by default
    @classmethod
    def run(self):
        """default method that will be executed by /core/brain/main.py"""
        import subprocess
        import logging
        from core.config import settings

        proc = subprocess.Popen(
            ["ffmpeg", "-f", "mjpeg", "-s", "320x240", "-i"], "/dev/video0", "%sout.mpg" % settings.APP_DIRS['tmp_input_video_dir']
            ,shell=False
            ,stdin=subprocess.PIPE
            ,stdout=subprocess.PIPE
            ,stderr=subprocess.PIPE
        )
        logging.info('Start video recording...')
        output, err = proc.communicate()
        logging.info("%s ", output)
        logging.info("%s", err)
        return True
