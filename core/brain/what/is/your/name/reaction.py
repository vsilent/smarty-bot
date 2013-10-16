from core.config import settings

class Reaction:
    """class Reaction"""

    request = ''
    req_from = ''
    response = ''

    def __str__(self):
        return 'Reaction on what is your name request'

    @classmethod
    def __init__(self, *args, **kwargs):
        """ original request string """
        #logger.info(args)
        #logger.info(kwargs)
        #logger.info(kwargs.get('req_obj'))
        req_obj = kwargs.pop('req_obj')
        self.request = req_obj.get('request', '')
        #request from (julius, jabber any other resources)
        self.req_from = req_obj.get('from', '')
        self.response = ''

    @classmethod
    def run(self):
        """default method"""

        if self.req_from == 'jabber':
            response = 'My name is, ' + settings.MY_NAME.upper()
            todo = { 'text' : response, 'jmsg' : response, 'type': 'response' }

        if self.req_from == 'julius':
            todo = { 'say': response , 'text' : response ,'type': 'response' }

        #settings.logger.debug('Reaction: %s' % todo)
        self.response = todo
        return self.response
