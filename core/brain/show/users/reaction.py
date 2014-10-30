from core.broadcast import say, bang
from core.people.person import Profile, Session


class Reaction:
    """class Reaction"""
    response = ''
    request = ''

    def __str__(self):
        return 'My new reaction'

    @classmethod
    def __init__(self, *args, **kwargs):
        """ original request string """

        #get request object
        self.req_obj = kwargs.pop('req_obj')

        #request word sequence
        self.request = str(self.req_obj.get('request', ''))

        #request received from (julius, jabber any other resources)
        self.req_from = self.req_obj.get('from', '')

        self.response = ''

    @classmethod
    def run(self):
        """default method"""

        email = None
        sess = Session()
        sender = self.req_obj.get('sender', '')

        #exctract sender email
        if sender:
            email = sender.split('/')[0]

        uuid = self.req_obj.pop('uuid', '')

        if email:
            #find user profile by primary email
            profile = sess.query(Profile).filter(Profile.email == email).one()
        elif uuid:
            #find user profile by uuid
            profile = sess.query(Profile).filter(Profile.uuid == uuid).one()

        if profile.type == 'admin' and self.req_from == 'jabber':
            users = sess.query(Profile).filter().all()
            user_list = ['%s %s %s %s' % (
                u.first_name, u.last_name, u.nickname, u.email
            ) for u in users]

            if user_list:
                response = "\n".join(user_list)
            else:
                response = 'No users found'
        else:
            response = 'Sorry, only admins can see that'

        #########################################
        # If reaction executed by jabber client #
        #########################################

        if self.req_from == 'jabber':
            todo = {'text': response, 'jmsg': response, 'type': 'response'}
            self.response = todo

        #########################################
        # If reaction executed by julius client #
        #########################################

        if self.req_from == 'julius':
            bang()
            todo = {'say': response, 'text': response, 'type': 'response'}
            self.response = say(self.request.replace('say', '').upper())

        return self.response
#n = Reaction(*{'reserved':''}, **{'req_obj':{'from':'', 'request':''}})
#n.run()
