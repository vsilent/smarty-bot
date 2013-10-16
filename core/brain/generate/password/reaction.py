
'''
Author:
Description:
'''
from core.broadcast import say, bang
from core.people.person import Profile
from core.people.person import Session
from core.config.settings import logger
import random
import string


class Reaction:
    """class Reaction"""

    response = ''
    request = ''
    profile = None

    def __str__(self):
        return 'My new reaction'

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

    @classmethod
    def run(self):
        """default method"""

        sender = self.req_obj.get('sender', '')
        uuid = self.req_obj.get('uuid', '')

        #######################################################################
        #                                                                     #
        #                        get user profile                             #
        #                                                                     #
        #######################################################################

        sess = Session()

        #exctract sender email
        if sender:
            email = sender.split('/')[0]
            if email:
                #find user profile by primary email
                self.profile = sess.query(Profile).filter(
                    Profile.email == email).one()
        elif uuid:
            #find user profile by uuid
            self.profile = sess.query(
                Profile).filter(Profile.uuid == uuid).one()

        logger.info(self.profile.email)

        #######################################################################
        #                                                                     #
        #                        prepare response                             #
        #                                                                     #
        #######################################################################

        myrg = random.SystemRandom()
        length = 10
        # If you want non-English characters, remove the [0:52]
        alphabet = string.letters[0:52] + string.digits
        pw = str().join(myrg.choice(alphabet) for _ in range(length))
        response = pw

        if self.req_from == 'jabber':
            todo = {'text': response, 'jmsg': response, 'type': 'response'}
            self.response = todo

        if self.req_from == 'julius':
            bang()
            todo = {'say': response, 'text': response, 'type': 'response'}
            self.response = say(self.request.replace('say', '').upper())

        return self.response

        #######################################################################
        #                                                                     #
        #                 cd ~/smarty and run python console.py               #
        #                                                                     #
        #######################################################################

        #direct test
        #r = Reaction(**{'req_obj':{'request': '',
                                    #'from' : '',
                                    #'sender': 'your.name@gmail.com'}})
        #r.run()
