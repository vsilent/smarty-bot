from core.config.settings import logger

'''
Author:
Description:
'''


class Reaction:

    def __str__(self):
        """ """
        return 'This class provides .... '

    @classmethod
    def __init__(self, *args, **kwargs):
        """ original request string """
        logger.info(args)
        logger.info(kwargs)
        logger.info(kwargs.get('req_obj'))
        self.request = kwargs.pop('req_obj')['request']
        self.response = None

    @classmethod
    def continue_dialog(self):
        """ False will stop dialog after processing run() method  and start new from begining
            otherwise will continue to store request
        """
        return True

    #this method will be executed by default
    @classmethod
    def run(self, request):
        """default method that will be executed by /core/brain/main.py and receives custom request string / command arguments"""

import resource, os

while True:
    print "CPU limit of child (pid %d)" % os.getpid(), resource.getrlimit(resource.RLIMIT_CPU)
    pass
