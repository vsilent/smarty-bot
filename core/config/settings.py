#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""  Main configuration file  """

import os
import sys
import logging
import logging.handlers
import multiprocessing
from unipath import Path

MY_NAME = 'smarty'

#for session
SECRET_KEY = 'yoursecretkeytypeanystring'

#Robot's gmail account
MY_ACCOUNTS = {'gmail': {'email': 'bot@gmail.com',
                         'password': 'botpassword'}}

REDIS = {
    'password': 'test',
    'socket': '/var/run/redis/redis.sock'
}

GOOGLE = {
    'google_talk_server': 'talk.google.com',
    'google_talk_server_port': '443',
    'google_app_name': 'googleappname',
    'google_app_password': 'googleapppassword',
}


TWITTER = {
    'consumer_key': '',
    'consumer_secret': '',
    'access_token_key': '',
    'access_token_secret': '',
}

LINKEDIN = {
    'consumer_key': '',
    'consumer_secret': '',
    'access_token_key': '',
    'access_token_secret': '',
    'return_url': 'http://www.smarty-bot.com'
}

REDMINE = {
    'url': '',
    'key': '',
    'username': '',
    'password': ''
}

SUGARCRM = {
    'url': 'h',
    'username': '',
    'password': ''
}
#database
DB = 'mysql+mysqldb://root@localhost/smarty'

PEOPLE = {
    'admin': {
        'email': 'youradmin@yourdomain.com'
    },
    'developer': {
        'email': 'developer@yourdomain.com'
    }
}

#HOME_DIR = os.path.expanduser('~')
ROBOT_DIR = Path(__file__).ancestor(3)
HOME_DIR = ROBOT_DIR.parent
LOG_DIR = ROBOT_DIR.child('core', 'var', 'log')
CONFIG_DIR = ROBOT_DIR.child('core', 'config')
TMP_DIR = '/tmp'
DEMO_MUSIC_DIR = ROBOT_DIR + '/music/'


FREEBASE = {
    "api_key": ''
}

if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

#try to create log file
file = open('%s/message.log' % LOG_DIR, 'w+')

# Make a global logging object.
logging.basicConfig(filename='%s/message.log' % LOG_DIR, level=logging.DEBUG)
logger = logging.getLogger("logfun")
logger.setLevel(logging.DEBUG)
hand = logging.StreamHandler()
f = logging.Formatter(
    "%(levelname)s %(asctime)s %(funcName)s %(lineno)d %(message)s")
hand.setFormatter(f)

logger = logging.getLogger()

smtp_handler = logging.handlers.SMTPHandler(
    mailhost=("smtp.gmail.com", 587),
    fromaddr=MY_ACCOUNTS['gmail']['email'],
    toaddrs=PEOPLE['admin']['email'],
    subject=u"%s error!" % MY_NAME,
    credentials = (
        MY_ACCOUNTS['gmail']['email'],
        MY_ACCOUNTS['gmail']['password']
    ),
    secure=()
)

#inform about exceptions only
smtp_handler.setLevel(logging.ERROR)
logger.addHandler(smtp_handler)
logger.addHandler(hand)

multiprocessing.log_to_stderr(logging.DEBUG)

SPEECH_RECOGNITION_ENABLED = True
JABBER_ENABLED = True
WEBSOCK_ENABLED = True

APP_DIRS = {
    'config_dir': CONFIG_DIR
    ,'lib_dir': CONFIG_DIR + "/../lib/"
    ,'app_dir': CONFIG_DIR + "/../"
    ,'tmp_input_audio_dir': CONFIG_DIR  + "/../tmp/input/audio/"
    ,'tmp_output_audio_dir': CONFIG_DIR  + "/../tmp/output/audio/"
    ,'tmp_input_video_dir': CONFIG_DIR  + "/../tmp/input/video/"
    ,'audio_dir': CONFIG_DIR  + "/../var/dict/audio/"
    ,'brain_modules_dir': CONFIG_DIR  + "/../brain/"
}

PLAYER_PATH = '/usr/bin/mplayer'

INSTALLED_LIBS = (
    'Skype4Py',
)

sys.path.append(os.path.dirname(APP_DIRS['app_dir']))
sys.path.append(os.path.dirname(APP_DIRS['config_dir']))
sys.path.append(ROBOT_DIR)

for lib in INSTALLED_LIBS:
    sys.path.append(
        os.path.dirname(APP_DIRS['lib_dir'] + lib + '/')
    )


DEVICES = {
    # Your capture device, use arecord -L to retrieve the one you use
    'audio_input': "default",
    'audio_output': "default"
}


#greetings must be a tuple
#will be moved to separate dictionary or refactored later
GREETINGS = (
    'hello'
    , 'Hello'
    , 'hey'
    , 'yo'
    , 'morning'
    , 'good morning'
    , 'good afternoon'
    , 'good day'
    , 'good evening'
    , 'hello'+ MY_NAME
    , 'hey '+ MY_NAME
)

#will be moved to separate dictionary or refactored later
S_QUESTIONS = (
    "what"
    ,"what is"
    ,"what are"
    ,"where is"
    ,"where are"
    ,"where he"
    ,"where you"
    ,"where"
    ,"where it"
    ,"who is"
    ,"who are"
    ,"who"
    ,"whose is"
    ,"whose are"
    ,"whose"
    ,"which is"
    ,"which are"
    ,"which"
    ,"was it"
    ,"was she"
    ,"was he"
    ,"was"
    ,"wasn't"
    ,"how"
    ,"when"
    ,"were"
    ,"why"
    ,"do"
    ,"don't"
    ,"did"
    ,"didn't"
    ,"does"
    ,"doesn't"
    ,"have"
    ,"haven't"
    ,"had"
    ,"hadn't"
    ,"has"
    ,"hasn't"
    ,"can"
    ,"can't"
    ,"could"
    ,"couldn't"
    ,"are"
    ,"is"
    ,"isn't"
    "aren't" )

E_QUESTIONS = (
    "are you"
    ,"aren't you"
    ,"do i"
    ,"do you"
    ,"do we"
    ,"do they"
    ,"does she"
    ,"does he"
    ,"does it"
    ,"doesn't it"
    ,"doesn't he"
    ,"doesn't she"
    ,"don't you"
    ,"have you"
    ,"have we"
    ,"have they"
    ,"have it"
    ,"haven't you"
    ,"are they"
    ,"isn't you"
    ,"did you"
    ,"didn't you"
)

#common polite questions
POLITE = (
    'whould you mind',
    'could you please',
    'please',
    'would you please',
    'can you please',
    'can you tell me',
    'could you tell me',
    'i wonder if',
    MY_NAME,
    MY_NAME.lower()
)

#actually this is the weak place in command recognition mechanism
#if you have some better ideas we would really appreciate to hear them
#these are simple commands that will be executed by
#first word in requested sentense like "say hello"

#  This tuple still exists because I did not have time to make it better.
#  It contains commands that have arguments.
#  Example: after "delete link" an argument
#  should follow, like: delete link mysite.com
#  If you have any other elegant and simple solution which may replace
#  this ugly dictionary please post a comment on github or fork.
#
EMBEDDED_COMMANDS = (
    MY_NAME
    , 'hi'
    , 'say'
    , 'send jabber message'
    , 'receive'
    , 'put'
    , 'read'
    , 'repeat'
    , 'message'
    , 'play music'
    , 'upgrade'
    , 'update me every day with'
    , 'update me every hour with'
    , 'update me each'
    , 'update me in'
    , 'update me at'
    , 'update me before'
    , 'update me after'
    , 'update me during'
    , 'update me on'
    , 'update me next'
    , 'update me tomorrow'
    , 'update'
    , 'help'
    , 'turn'
    , 'sneeze'
    , 'tweet'
    , 'ip'
    , 'my name is'
    , 'my zip is'
    , 'my zipcode is'
    , 'my zip code is'
    , 'my post code is'
    , 'my postcode is'
    , 'add site url'
    , 'add my site url'
    , 'add url'
    , 'add link'
    , 'add new url'
    , 'add new link'
    , 'add new site url'
    , 'add user'
    , 'add new user'
    , 'create user'
    , 'create new user'
    , 'create new reaction'
    , 'add'
    , 'remind me every day with'
    , 'remind me after'
    , 'remind me at'
    , 'remind me before'
    , 'remind me during'
    , 'remind me each'
    , 'remind me every'
    , 'remind me hourly'
    , 'remind me in the morning'
    , 'remind me in the afternoon'
    , 'remind me in the midnight'
    , 'remind me in'
    , 'remind me monthly'
    , 'remind me next'
    , 'remind me on'
    , 'remind me once'
    , 'remind me today'
    , 'remind me tomorrow'
    , 'remind me twice'
    , 'remind me weekly'
    , 'remind me with'
    , 'remind me yearly'
    , 'inform me every'
    , 'inform me each'
    , 'inform me in'
    , 'inform me at'
    , 'inform me before'
    , 'inform me after'
    , 'inform me during'
    , 'inform me on'
    , 'inform me next'
    , 'inform me tomorrow'
    , 'invite to gtalk'
    , 'notify me every'
    , 'notify me each'
    , 'notify me in'
    , 'notify me at'
    , 'notify me before'
    , 'notify me after'
    , 'notify me during'
    , 'notify me on'
    , 'notify me next'
    , 'notify me tomorrow'
    , 'msg me every'
    , 'msg me each'
    , 'msg me in'
    , 'msg me at'
    , 'msg me before'
    , 'msg me after'
    , 'msg me during'
    , 'msg me on'
    , 'msg me next'
    , 'msg me tomorrow'
    , 'message me'
    , 'ping me'
    , 'alert me'
    , 'who is'
    , "whois"
    , 'delete link'  #  because after delete link an argument follows, like: delete link mysite.com
    , 'delete url'
    , 'delete site url'
    , 'remove url'
    , 'remove site url'
    , 'remove link'
    , 'remove'
    , 'find'
    )

MSG_ME = (
    'remind me with message',
    'update me with message',
    'notify me with message',
    'alert me with message',
    'message me with',
    'msg me with',
    'update me with ',
    'notify me with',
    'alert me with',
    'with message',
    'with msg',
    'remind with',
    'update with',
    'alert with',
    'send me',
    'with message'
    'with msg'
    'with txt'
    'with text'
    'with'
    'by'
    'to',
    'of',
)
