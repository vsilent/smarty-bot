from core.config.settings import logger
from core.broadcast import output
from datetime import datetime

class Reaction:
    """class Reaction"""

    response = ''

    def __str__(self):
        return 'Reac'

    @classmethod
    def __init__(self, *args, **kwargs):
        """ original request string """
        #logger.info(kwargs)
        req_obj = kwargs.pop('req_obj')
        self.request = req_obj.get('request', '')

        #request from (julius, jabber any other resources)
        self.req_from = req_obj.get('from', '')

    @classmethod
    def run(self):
        """default method that executes by /core/brain/main.py and receives request string"""
        #use subprocess for your bindings when develop a new functionality
        fulldate = datetime.utcnow().strftime("%A, %d. %B %Y %I:%M%p")

        hours = datetime.utcnow().strftime("%I")
        minutes = datetime.utcnow().strftime("%I")

        if self.req_from == 'jabber':
            response = {'request': self.request
                        ,'text' : fulldate
                        ,'jmsg' : fulldate
                        ,'continue' : 0
                        ,'type':'response' }

        if self.req_from == 'julius':
            response = {'request': self.request
                        ,'say': "IT'S, %d O'CLOCK AND %d MINUTES" % ( int(hours), int(minutes))
                        ,'text' : fulldate
                        ,'continue' : 0
                        ,'type' : 'response' }

        return response
        #import subprocess
        #s = subprocess.Popen(['ffmpeg', '-i', speech, flac ] , stderr=subprocess.STDOUT, stdout=subprocess.PIPE).communicate()[0]
