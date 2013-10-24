import simplejson as json
import urllib
#from core.lib.wikipedia.simplemediawiki import MediaWiki
from core.config.settings import logger


# This example request includes an optional API key which you will need to
# remove or replace with your own key.
# Read more about why it's useful to have an API key.
# The request also includes the userip parameter which provides the end
# user's IP address. Doing so will help distinguish this legitimate
# server-side traffic from traffic which doesn't come from an end-user.

def search(text_to_search):
    """docstring for sear"""
    #wiki = MediaWiki('http://en.wikipedia.org/w/api.php')
    #results = wiki.call({
    #'action': 'query', 'prop': 'revisions', 'titles': 'Main Page'})
    #url = 'http://en.wikipedia.org/w/api.php?action=opensearch&search='+ \
    #urllib.urlencode({ 'q' : text_to_search }) + '&format=json';

    # of course I can try search on wikipedia.org but it does not work yet , so
    # using google
    url = 'http://ajax.googleapis.com/ajax/services/search/web?v=1.0&' +\
        urllib.urlencode({'q': text_to_search + ' wikipedia'})
    try:
        response = urllib.urlopen(url)
    except Exception as e:
        logger.exceprion(e)
        return False

    ## Process the JSON string.
    results = json.load(response)
    return results
