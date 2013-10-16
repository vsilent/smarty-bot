#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""

Speech recognition module
based on google service

"""

import os
from core.config import settings
from core.config.settings import logger
import pycurl
import StringIO
import simplejson as json
#import subprocess


def get_audio_file():
    """docstring for get_oldest_file"""
    search_dir = settings.APP_DIRS['tmp_input_audio_dir']
    files = filter(os.path.isfile, os.listdir(search_dir))
    if files is None:
        return False
    files = [os.path.join(search_dir, f) for f in files]
    files.sort(key=lambda x: os.path.getmtime(x))
    return files[:1][0]


def recognize():
    url = "https://www.google.com/speech-api/v1/recognize?xjerr=1&client=chromium&lang=en-US"
    res = StringIO.StringIO()
    c = pycurl.Curl()
    c.setopt(c.POST, 1)
    c.setopt(c.URL, url)
    flac = settings.APP_DIRS['tmp_input_audio_dir'] + 'speech.flac'
    c.setopt(pycurl.HTTPHEADER, ["Content-Type: audio/x-flac; rate=16000"])
    c.setopt(c.HTTPPOST, [(flac, (c.FORM_FILE, "speech.flac"))])
    c.setopt(pycurl.WRITEFUNCTION, res.write)
    c.perform()
    c.close()
    rcvdjson = res.getvalue()
    logger.debug('what google say' + rcvdjson)
    return json.loads(rcvdjson)['hypotheses'][0]


def record(device):
    os.system('arecord -D %s -t wav -r 44000 > %s/speech.wav' % (
        device, settings.APP_DIRS['app_dir'])
    )


def toflac():
    #@todo should use memory for future not filesystem
    flac = settings.APP_DIRS['tmp_input_audio_dir'] + 'speech.flac'
    speech = get_audio_file()
    #remove previous dialog flac file
    os.system('rm -f %s' % flac)
    #logger.debug(speech)
    #logger.debug(flac)
    os.system('%s/voice-cleanup.sh %s %s' % (settings.ROBOT_DIR, speech, flac))
    if not os.path.isfile(flac):
        raise 'COULD NOT CONVERT FLAC'
    return True


# first request
def recognize_by_google():
    os.chdir(settings.APP_DIRS['tmp_input_audio_dir'])
    try:
        toflac()
    except Exception as e:
        logger.exception(e)
        raise RuntimeError(',OOPS?')

    confidence = ''
    logger.info("Sending your speech to the Google.")
    try:
        utterance = recognize()['utterance']
        confidence = recognize()['confidence']
    except Exception as e:
        logger.exception(e)
        raise RuntimeError('INTERNET CONNECTION FAILED')

    logger.debug("Confidence: ", str(confidence))
    return utterance


def finish_dialog():
    """docstring for fini"""
    pass
