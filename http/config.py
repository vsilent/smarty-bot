#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""  Main configuration file  """

from unipath import Path

DEBUG = True

REDIS = {
    'host': 'redis',
    # 'password': 'test'
}

CACHE_TIMEOUT = 300
ROOT_DIR = Path(__file__).ancestor(1)
UPLOAD_FOLDER = ROOT_DIR + '/var/uploads/'

# max upload 6 Mb
MAX_CONTENT_LENGTH = 6 * 1024 * 1024

HOME_DIR = ROOT_DIR.parent
TMP_DIR = '/tmp'

TESTING = False
ADMINS = frozenset(['your.gmail@gmail.com'])
SECRET_KEY = 'hereisyoursecretkey'

# You must configure these 3 values from Google APIs console
# https://code.google.com/apis/console
GOOGLE_CLIENT_ID = ''
GOOGLE_CLIENT_SECRET = ''
REDIRECT_URI = '/'  # one of the Redirect URIs from Google APIs console

SQLALCHEMY_DATABASE_URI = 'mysql+mysqldb://root:root@localhost/smarty'
DATABASE_CONNECT_OPTIONS = {}

THREADS_PER_PAGE = 8

SECURITY_POST_LOGIN = '/users/dashboard'

CSRF_ENABLED = True
CSRF_SESSION_KEY = "somethingimpossibletoguesshere"

MAIL_SERVER = 'localhost'
MAIL_PORT = 25
MAIL_USE_TLS = False
MAIL_USE_SSL = False
MAIL_DEBUG = DEBUG
MAIL_USERNAME = None
MAIL_PASSWORD = None
MAIL_DEFAULT_SENDER = None
MAIL_MAX_EMAILS = None
MAIL_SUPPRESS_SEND = TESTING
