from core.broadcast import say, bang
from core.config.settings import logger

class Reaction:
    """class Reaction"""
    request = ''
    response = ''

    def __str__(self):
        return 'Say command reaction'

    def __init__(self, *args, **kwargs):
        """ original request string """

        #logger.info(kwargs)
        #logger.info(kwargs.get('req_obj'))
        self.request = kwargs.pop('req_obj')['request']
        self.response = None

    @classmethod
    def continue_dialog(self):
        """ False will stop current dialog after this reaction and start new from begining
            otherwise will continue to store request
        """
        return False

    @classmethod
    def run(self):
        """default method"""
        bang()
        logger.info(self.request)
        self.response = say(self.request.replace('say', '').upper())
        return self.response
