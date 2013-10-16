import logging
#from core.output import say
from core.config.settings import logger, DEMO_MUSIC_DIR
import subprocess
import os, random

class Reaction:
    """class Reaction"""
    def __str__(self):
        return 'Reac'

    @classmethod
    def __init__(self, *args, **kwargs):
        """ original request string """
        logger.info(args)
        logger.info(kwargs)
        logger.info(kwargs.get('req_obj'))
        self.request = kwargs.pop('req_obj')['request']
        self.response = None

    def continue_dialog(self):
        """ False will stop current dialog after this reaction and start new from begining
            otherwise will continue to store request
        """
        return False

    #def run(self, request):
        #"""default method"""
        #from core.output import say
        #from core.config.settings import DEMO_MUSIC_DIR
        #import logging
        #say('OK')
        #import os
        #import subprocess
        #logging.debug('Playing... %s ' % DEMO_MUSIC_DIR)
        #os.system('mplayer ' + DEMO_MUSIC_DIR +'*.wav')
        #return True

    def run(self, request):
        """default method"""

        file = DEMO_MUSIC_DIR + random.choice( os.listdir( DEMO_MUSIC_DIR ) )
        logger.info('Playing... %s ' % file )

        proc = subprocess.Popen(
             [ "/usr/bin/mplayer", file ]
        )
        #stdoutdata, stderrdata = proc.communicate()
        #logging.info('Start subprocess...%s', proc.pid)
        return True
