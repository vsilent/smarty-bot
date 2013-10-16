class Reaction:
    """class Reaction"""
    def __str__(self):
        return 'Reac'

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

    def continue_dialog(self):
        """ False will stop dialog after processing run()
        method  and start new from begining
            otherwise will continue to store request
        """
        return False

    def run(self, request):
        """default method that executes by /core/brain/main.py
        and receives request string"""
        return True
