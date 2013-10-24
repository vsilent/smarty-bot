import urllib

class Wiki:
    """class Wiki"""

    def __str__(self):
        return 'Wiki'

    def __init__(self):
        pass

    def find_resourse_link(self, results):
        """docstring for find_resourse_link"""
        for i in results['responseData']['results']:
            if( 'http://en.wikipedia.org/wiki/' in i['url']  ):
                return i['url']
            else:
                return False;

    #find audio resource
    def find_audio_resourse(self, link):
        """docstring for find_audio_resourse"""
        link_to_audio = False
        #link_to_audio = 'http://wiki/images/google.wav'
        return link_to_audio
