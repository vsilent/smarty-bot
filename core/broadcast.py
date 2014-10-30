#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Defaul output lib
"""

import os
from core.config.settings import logger
from core.utils.utils import Utils
from core.config import settings
import subprocess
import zmq
from core.lib import speechd


def bang():
    comm = ["aplay",
            "%salert.wav" % settings.APP_DIRS['tmp_output_audio_dir']]
    """docstring for bang"""
    try:
        subprocess.Popen(comm)
    except OSError as e:
        if e.errno == os.errno.ENOENT:
            # handle file not found error.
            logger.info('Looks like play is not installed')
            logger.exception(e)
        else:
            # Something else went wrong while trying to run `wget`
            pass


def say(what_to_say):
    """ use linux synthezer"""
    client = speechd.SSIPClient('test')
    client.set_output_module('festival')
    client.set_language('en')
    client.set_punctuation(speechd.PunctuationMode.SOME)
    client.speak(what_to_say)
    client.close()
    return {'text': 'Saying it..'}


def play(text):
    """docstring for play"""
    _utils = Utils()
    path = _utils.get_full_path_to_info_by_sentense(text)
    info = _utils.load_file_json_info(path)
    if os.path.isfile(info['audio_local']):
        logger.info("play audio %s .." % info['audio_local'])
        subprocess.Popen(
            ["play", "%" % info['audio_local']]
        )
    elif(os.path.isfile(path + '/audio.wav')):
        logger.info("play audio %s .." % path)
        subprocess.Popen(
            ["play", "%" % path + '/audio.wav']
        )


def output(req_obj):
    """docstring for outp"""
    pass
    #context = zmq.Context()
    #sock = context.socket(zmq.PUB)
    #sock.bind('ipc:///tmp/smarty-output')
    #logger.info('Send to output %s' % req_obj)
    #req_obj = sock.send_json(req_obj)
