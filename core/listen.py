"""
Auxiliary functions

"""

from core import record as recorder
from core.utils.utils import Utils
from core.config import settings
import subprocess


def listen():
    """ record audio from microphone"""
    utils = Utils()
    utils.clean_input_audio_dir()
    fname = recorder.record_to_file()
    settings.logger.info("result written to %s.wav" % fname)


def reset_input():
    """ remove all audio from tmp/input/audio"""
    subprocess.Popen(
        ["rm", "-f", settings.APP_DIRS['tmp_input_audio_dir'] + '*.wav ']
    )
