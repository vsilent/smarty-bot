__author__ = 'vs@webdirect.md'


class Response(object):
    """
    Primitive response object
    """
    _plain = ''
    _text = ''
    _msg = None
    _request = None
    _from = None
    _continue = None
    _sender = None
    _jmsg = None
    _type = None

    def __init__(self):
        pass

    def __new__(cls, **kwargs):
        cls._request = kwargs.get('request', None)
        cls._from = kwargs.get('from', None)
        cls._plain = kwargs.get('plain', '')
        cls._html = kwargs.get('html', cls._plain)
        cls._text = kwargs.get('text', cls._plain)
        cls._continue = kwargs.get('continue', None)
        cls._jmsg = kwargs.get('jmsg', cls._text)
        cls._type = kwargs.get('type', 'response')

        return {
            'request': cls._request,
            'from': cls._from,
            'text': cls._text,
            'plain': cls._plain,
            'html': cls._html,
            'continue': cls._continue,
            'jmsg': cls._jmsg,
            'type': cls._type,
        }
