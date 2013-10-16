import twitter
from core.config.settings import TWITTER


def tweet(msg):
    """docstring for tweet"""
    api = twitter.Api(TWITTER['consumer_key'], TWITTER['consumer_secret'], TWITTER['access_token_key'], TWITTER['access_token_secret'])
    print api.VerifyCredentials()
    print api.VerifyCredentials()
    #statuses = api.GetPublicTimeline()
    #users = api.GetFriends()
    #print [u.name for u in users]
    status = api.PostUpdate(msg)
    return status.text
