#!/usr/bin/env python
# -*- coding: utf-8 -*-
class Reaction:
    """class Reaction"""
    response = ''
    request = ''

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

        response = "\
        Let's say you need a similar reaction to 'core/brain/play/music/reaction.py' but\
        with a bit difference for example: 'core/brain/play/my/music/reaction.py'\
        just create file in core/brain/play/my/music/reaction.py and put the following lines:\n\n \
        from core.brain.play.music import Reaction                                   \
        class ReactionCopy(Reaction):                                                 \
            def __init__(self, *args, **kwargs):                                      \
                                                                                      \
                super(ReactionCopy, self).__init__()                                  \
                                                                                      \
                if self.req_from == 'jabber':                                         \
                    todo = {'text': response, 'jmsg': response, 'type': 'response'}   \
                    self.response = todo                                              \
                                                                                      \
                if self.req_from == 'julius':                                         \
                    bang()                                                            \
                    todo = {'say': response, 'text': response, 'type': 'response'}    \
                    self.response = say(self.request.replace('say', '').upper())      \
                return self.response                                                  \
       "
