#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Recognize module
"""

import os
from core.config import settings
from core.config.settings import logger
import pycurl
import StringIO
import simplejson as json
#import subprocess
from broadcast import say


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
    os.system('arecord -D %s -t wav -r 44000 > %s/speech.wav' % ( device , settings.APP_DIRS['app_dir']))


def toflac():
    flac = settings.APP_DIRS['tmp_input_audio_dir'] + 'speech.flac'
    speech = get_audio_file()
    #remove previous dialog flac file
    os.system('rm -f %s' % flac )
    logger.debug(speech)
    logger.debug(flac)
    os.system('%s/voice-cleanup.sh %s %s' % (settings.ROBOT_DIR, speech, flac))
    #s = subprocess.Popen(['ffmpeg', '-i', speech, flac ] , stderr=subprocess.STDOUT, stdout=subprocess.PIPE).communicate()[0]
    #logger.debug(s)
    #os.system('rm -f %s' % speech )
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


def meet():
    """docstring for meet"""
    pass


def finish_dialog():
    """docstring for fini"""
    pass


def recognize_by_julius():
    #not in use anymore because requires X11, used fifo instead
    #bus = dbus.SessionBus()
    #service = bus.get_object('com.optibot.julius', '/com/optibot/julius')
    #jlisten = service.get_dbus_method('listen', 'com.optibot.julius')
    #res = jlisten()
    filename = os.path.join('/tmp', 'julius_fifo')
    fifo = open(filename, 'r')
    return fifo.readline()


def is_yes_or_no(n=1):
    """docstring for yes_or_no"""
    #@todoREEEEEESSSSSSSSSSSEEEEEEEEETTTTTTT curently it's not working properly
    #reset_julius()
    #text = recognize_by_julius()
    if text:
        if text.lower() in ['yes', 'no', 'ok', 'sure']:
            return True


def yes_or_no(n=1):
    """docstring for yes_or_no"""
    #@todoREEEEEESSSSSSSSSSSEEEEEEEEETTTTTTT curently it's not working properly
    #reset_julius()
    #text = recognize_by_julius()
    if text:
        logger.debug(text)

        if text.lower() in ['yes', 'no', 'ok', 'sure']:
            return text.lower()

        if text.lower() not in ['yes', 'no', 'ok', 'sure']:
            say('Yes, or No ?')
            #reset_julius()

        n += 1
        if n > 3:
            return 'no'
        yes_or_no()


#@deprecated
def reset_julius():
    """julius has a python wrapper lib so we don't need this function anymore."""
    pass
    #if os.path.isfile('/tmp/julius_fifo'):
        #filename = os.path.join('/tmp', 'julius_fifo')
        #fifo = open(filename, 'r')
        #fifo.readlines()
