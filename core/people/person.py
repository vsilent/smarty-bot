#!/usr/bin/env python
# -*- coding: utf-8 -*-
from sqlalchemy import create_engine, Table
from sqlalchemy import Column, Integer, String, DateTime, Date
from sqlalchemy import MetaData, UnicodeText, text, Index
from sqlalchemy.orm import mapper, sessionmaker, scoped_session
#from sqlalchemy.sql import select
import uuid
import hashlib
from core.config.settings import logger
from core.config.settings import DB
import datetime

engine = create_engine(DB, echo=False, pool_recycle=3600)
metadata = MetaData()
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
#metadata = MetaData(bind=engine, reflect=True)

account_table = Table(
    'account',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('uuid', String(36)),
    Column('password', String(200)),
    mysql_engine='InnoDB',
    mysql_charset='utf8')

profile_table = Table(
    'account_profile',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('account_id', String(36), primary_key=True),
    Column('uuid', String(255)),
    Column('email', String(255), nullable=True),
    Column('first_name', String(255), nullable=True),
    Column('last_name', String(255), nullable=True),
    Column('birthdate', Date, nullable=True),
    Column('birthplace', String(255), nullable=True),
    Column('nationality', String(255)),
    Column('nickname', String(24), nullable=True),
    Column('gender', String(255), nullable=True),
    Column(
        'priority', String(11),
        nullable=True,
        default=text(u"'0'"),
        server_default=text('NULL')),
    Column('type', String(8), nullable=True),
    Column('age', Integer(), nullable=True, default=text(u"'0'")),
    Column('sign', String(11), nullable=True),
    Column('first_login', Integer(), nullable=True, default=text(u"'0'")),
    Column('last_login', Integer(), nullable=True, default=text(u"'0'")),
    Column('registered', Integer(), nullable=True, default=text(u"'0'")),
    Column('updated', Integer(), nullable=True, default=text(u"'0'")),
    Column('homepage', String(255), nullable=True),
    Column('home_country', String(255), nullable=True),
    Column('home_city', String(255), nullable=True),
    Column('home_state', String(255), nullable=True),
    Column('home_street', String(255), nullable=True),
    Column('home_house', String(255), nullable=True),
    Column('home_apartment', String(255), nullable=True),
    Column('home_postcode', String(255), nullable=True),
    Column('home_phone', String(255), nullable=True),
    Column('work_country', String(255), nullable=True),
    Column('work_city', String(255), nullable=True),
    Column('work_street', String(255), nullable=True),
    Column('work_house', String(255), nullable=True),
    Column('work_postcode', String(255), nullable=True),
    Column('work_phone', String(255), nullable=True),
    Column('mobile_phone', String(255), nullable=True),
    Column('music', String(16), nullable=True),
    Column('food', String(16), nullable=True),
    Column('drink', String(16), nullable=True),
    Column('location_id', Integer(), nullable=True),
    Column('status', String(255), nullable=True),
    Column('online', Integer(1), nullable=True),
    mysql_engine='MyISAM',
    mysql_charset='utf8'
)

Index('id', profile_table.c.id, unique=True)
Index('uuid', profile_table.c.uuid, unique=True)
Index('email', profile_table.c.email, unique=True)
Index('first_name', profile_table.c.first_name)
Index('last_name', profile_table.c.last_name)
Index('nickname', profile_table.c.nickname)
Index('homepage', profile_table.c.homepage)
Index('mobile_phone', profile_table.c.mobile_phone, unique=False)
Index('location_id', profile_table.c.location_id)

profile_role_table = Table(
    'account_profile_role',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('uuid', String(255)),
    Column('role', String(255)),
    mysql_engine='MyISAM',
    mysql_charset='utf8')

Index('id', profile_role_table.c.id)
Index('uuid', profile_role_table.c.uuid)
Index('role', profile_role_table.c.role)

profile_social_table = Table(
    'account_profile_social',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('uuid', String(255)),
    Column('service_id', UnicodeText()),
    Column('service_name', String(255)),
    Column('service_url', UnicodeText()),
    Column('service_consumer_key', UnicodeText()),
    Column('service_consumer_secret', UnicodeText()),
    Column('service_access_token', UnicodeText()),
    Column('service_scope', UnicodeText()),
    Column('service_login', UnicodeText()),
    Column('service_email', String(255)),
    Column('service_password', UnicodeText()),
    Column('notes', UnicodeText()),
    mysql_engine='MyISAM',
    mysql_charset='utf8')

Index('id', profile_social_table.c.id)
Index('uuid', profile_social_table.c.uuid)


profile_interest_table = Table(
    'account_interest_email',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('uuid', String(255)),
    Column('interest', UnicodeText()),
    mysql_engine='MyISAM',
    mysql_charset='utf8'
)
Index('id', profile_interest_table.c.id)
Index('uuid', profile_interest_table.c.uuid)

profile_request_table = Table(
    'account_profile_request',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('uuid', String(255)),
    Column('request', String(255)),
    mysql_engine='MyISAM',
    mysql_charset='utf8'
)
Index('id', profile_request_table.c.id)
Index('uuid', profile_request_table.c.uuid)

profile_comment_table = Table(
    'account_profile_comment',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('uuid', String(255)),
    Column('comment', UnicodeText()),
    mysql_engine='MyISAM',
    mysql_charset='utf8'
)
Index('id', profile_comment_table.c.id)
Index('uuid', profile_comment_table.c.uuid)

profile_relation_table = Table(
    'account_profile_relation',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('uuid', String(255)),
    Column('type', String(255)),
    Column('related_account', UnicodeText()),
    Column('related_account_type', String(255)),
    mysql_engine='MyISAM',
    mysql_charset='utf8')

Index('id', profile_relation_table.c.id)
Index('uuid', profile_relation_table.c.uuid)

profile_other_name_table = Table(
    'account_profile_other_name',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('uuid', String(255)),
    Column('name', String(255)),
    mysql_engine='MyISAM',
    mysql_charset='utf8'
)
Index('id', profile_other_name_table.c.id)
Index('uuid', profile_other_name_table.c.uuid)
Index('name', profile_other_name_table.c.name)

profile_email_table = Table(
    'account_profile_email',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('uuid', String(255)),
    Column('email', String(255)),
    mysql_engine='MyISAM',
    mysql_charset='utf8'
)
Index('id', profile_email_table.c.id)
Index('uuid', profile_email_table.c.uuid)
Index('email', profile_email_table.c.email)

profile_picture_table = Table(
    'account_profile_picture',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('uuid', String(255)),
    Column('picture', String(255)),
    mysql_engine='MyISAM',
    mysql_charset='utf8'
)
Index('id', profile_picture_table.c.id)
Index('uuid', profile_picture_table.c.uuid)

profile_phone_table = Table(
    'account_profile_phone',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('uuid', String(255)),
    Column('phone', String(255)),
    mysql_engine='MyISAM',
    mysql_charset='utf8')
Index('id', profile_phone_table.c.id)
Index('uuid', profile_phone_table.c.uuid)

profile_cronjob_table = Table(
    'account_profile_cronjob',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('uuid', String(255)),
    Column('job', String(255)),
    mysql_engine='MyISAM',
    mysql_charset='utf8')
Index('id', profile_cronjob_table.c.id)
Index('uuid', profile_cronjob_table.c.uuid)

profile_device_table = Table(
    'account_profile_device',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('device_id', Integer(255)),
    mysql_engine='MyISAM',
    mysql_charset='utf8'
)
Index('id', profile_device_table.c.id, unique=True)
Index('device_id', profile_device_table.c.device_id, unique=True)

device_table = Table(
    'device',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('serial', String(255), nullable=True),
    Column('name', String(255)),
    Column('type', String(255), nullable=True),
    Column('model', String(255), nullable=True),
    Column('make', String(255), nullable=True),
    Column('built', String(255), nullable=True),
    Column('family', String(255), nullable=True),
    Column('desc', UnicodeText(), nullable=True),
    Column('params', UnicodeText(), nullable=True),
    Column('network_name', String(255), nullable=True),
    Column('mac_address', String(255), nullable=True),
    Column('location', String(255), nullable=True),
    mysql_engine='MyISAM',
    mysql_charset='utf8')
Index('id', device_table.c.id, unique=True)
Index('serial', device_table.c.serial, unique=True)
Index('name', device_table.c.name, unique=True)
Index('model', device_table.c.model, unique=True)
Index('mac_address', device_table.c.mac_address, unique=True)

country_table = Table(
    'country',
    metadata,
    Column('id', Integer(), primary_key=True, nullable=False),
    Column('iso', String(2), nullable=False),
    Column('name', String(80), nullable=False),
    Column('title', String(80), nullable=False),
    Column('iso3', String(3)),
    Column('numcode', Integer(1)),
    mysql_engine='MyISAM',
    mysql_charset='utf8')

profile_link_table = Table(
    'account_profile_link',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('uuid', String(255)),
    Column('type', String(255), nullable=True),
    Column('url', UnicodeText()),
    mysql_engine='MyISAM',
    mysql_charset='utf8')

Index('id', profile_link_table.c.id, unique=True)
#Index('uuid', profile_link_table.c.uuid, unique=True)

#needed for registering working hours
profile_timesheet_table = Table(
    'account_profile_timesheet',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('uuid', String(255)),
    Column('type', String(255), nullable=True),
    Column('created', DateTime, default=datetime.datetime.now),
    Column('spent', UnicodeText()),
    mysql_engine='MyISAM',
    mysql_charset='utf8')
Index('id', profile_timesheet_table.c.id, unique=True)
Index('uuid', profile_timesheet_table.c.id, unique=True)


company_table = Table(
    'company_profile',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String(255), nullable=False),
    Column('domain', String(255), nullable=True),
    Column('type', String(255), nullable=True),
    Column('registered', DateTime, default=datetime.datetime.now),
    Column('updated', DateTime, default=datetime.datetime.now),
    Column('founded', Integer(), nullable=True, default=text(u"'0'")),
    Column('homepage', String(255), nullable=True),
    Column('country', String(255), nullable=True),
    Column('city', String(255), nullable=True),
    Column('state', String(255), nullable=True),
    Column('street', String(255), nullable=True),
    Column('house', String(255), nullable=True),
    Column('postcode', String(255), nullable=True),
    Column('phone', String(255), nullable=True),
    Column('fax', String(255), nullable=True),
    Column('location_id', Integer(), nullable=True),
    Column('info', UnicodeText(), nullable=True),
    Column('status', String(255), nullable=True),
    mysql_engine='MyISAM',
    mysql_charset='utf8'
)

Index('id', company_table.c.id, unique=True)
Index('name', company_table.c.name)
Index('domain', company_table.c.domain, unique=False)


company_member_table = Table(
    'company_member_profile',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('company_id', String(255)),
    Column('uuid', String(255)),
    Column('email1', String(255), nullable=True),
    Column('email2', String(255), nullable=True),
    Column('registered', DateTime, default=datetime.datetime.now),
    Column('updated', DateTime, default=datetime.datetime.now),
    Column('homepage', String(255), nullable=True),
    Column('country', String(255), nullable=True),
    Column('city', String(255), nullable=True),
    Column('state', String(255), nullable=True),
    Column('street', String(255), nullable=True),
    Column('office', String(255), nullable=True),
    Column('postcode', String(255), nullable=True),
    Column('phone1', String(255), nullable=True),
    Column('phone2', String(255), nullable=True),
    Column('phone3', String(255), nullable=True),
    Column('cellphone1', String(255), nullable=True),
    Column('cellphone2', String(255), nullable=True),
    Column('cellphone3', String(255), nullable=True),
    Column('fax1', String(255), nullable=True),
    Column('fax2', String(255), nullable=True),
    Column('profession', UnicodeText(), nullable=True),
    Column('info', UnicodeText(), nullable=True),
    Column('location_id', Integer(), nullable=True),
    Column('status', String(255), nullable=True),
    mysql_engine='MyISAM',
    mysql_charset='utf8'
)

Index('id', company_member_table.c.id, unique=True)
Index('company_id', company_member_table.c.company_id, unique=True)
Index('email1', company_member_table.c.email1, unique=False)


profile_interaction_table = Table(
    'profile_interaction_history',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('uuid1', String(255)),
    Column('uuid2', String(255)),
    Column('email1', String(255), nullable=True),
    Column('email2', String(255), nullable=True),
    Column('registered', DateTime, default=datetime.datetime.now),
    Column('updated', DateTime, default=datetime.datetime.now),
    Column('type', String(255), nullable=True),
    Column('data', UnicodeText(), nullable=True),
    Column('status', String(255), nullable=True),
    mysql_engine='MyISAM',
    mysql_charset='utf8'
)

Index('id', profile_interaction_table.c.id, unique=True)
Index('uuid1', profile_interaction_table.c.uuid1, unique=True)
Index('uuid2', profile_interaction_table.c.uuid2, unique=True)
Index('email1', profile_interaction_table.c.email1, unique=False)
Index('email2', profile_interaction_table.c.email2, unique=False)
Index('type', profile_interaction_table.c.type, unique=False)


class ProfileTimesheet(object):

    def __init__(self, **kwargs):
        self.uuid = kwargs.pop('uuid')
        self.type = kwargs.pop('type')
        self.created = kwargs.pop('created')
        self.spent = kwargs.pop('spent')

    def __repr__(self):
        return "<ProfileTimesheet('%s')>" % (self.id)


class ProfileLink(object):
    def __init__(self, **kwargs):
        self.uuid = kwargs.pop('uuid')
        self.type = kwargs.pop('type')
        self.url = kwargs.pop('url')

    def __repr__(self):
        return "<ProfileLink('%s')>" % (self.url)


class Country(object):

    def __init__(self, **kwargs):
        self.id = kwargs.pop('id', '')
        self.iso = kwargs.pop('iso', '')
        self.name = kwargs.pop('name', '')
        self.title = kwargs.pop('title', '')
        self.iso3 = kwargs.pop('iso3', '')
        self.numcode = kwargs.pop('numcode', '')

    def __repr__(self):
        return "<Country('%s')>" % (self.iso)


class Account(object):
    def __init__(self, **kwargs):
        #self.id = kwargs.pop('id', '')
        self.uuid = kwargs.pop('uuid', '')
        self.password = kwargs.pop('password', '')

    def __repr__(self):
        return "<Account('%s', '%s')>" % (self.id, self.uuid)


class Profile(object):
    query = db_session.query_property()

    def __init__(self, **kwargs):
        self.uuid = kwargs.pop('uuid')
        self.email = kwargs.pop('email', '')
        self.first_name = kwargs.pop('first_name', '')
        self.last_name = kwargs.pop('last_name', '')
        self.birthdate = kwargs.pop('birthdate', 0)
        self.birthplace = kwargs.pop('birthplace', '')
        self.nationality = kwargs.pop('nationality', '')
        self.nickname = kwargs.pop('nickname', '')
        self.gender = kwargs.pop('gender', '')
        self.priority = kwargs.pop('priority', '')
        self.type = kwargs.pop('type', '')
        self.age = kwargs.pop('age', 0)
        self.sign = kwargs.pop('sign', '')
        self.first_login = kwargs.pop('first_login', '')
        self.last_login = kwargs.pop('last_login', '')
        self.registered = kwargs.pop('registered', 0)
        self.updated = kwargs.pop('updated', 0)
        self.homepage = kwargs.pop('homepage', '')
        self.home_country = kwargs.pop('home_country', '')
        self.home_city = kwargs.pop('home_city', '')
        self.home_state = kwargs.pop('home_state', '')
        self.home_street = kwargs.pop('home_street', '')
        self.home_house = kwargs.pop('home_house', '')
        self.home_apartment = kwargs.pop('home_apartment', '')
        self.home_postcode = kwargs.pop('home_postcode', '')
        self.home_phone = kwargs.pop('home_phone', '')
        self.work_country = kwargs.pop('work_country', '')
        self.work_city = kwargs.pop('work_city', '')
        self.work_street = kwargs.pop('work_street', '')
        self.work_house = kwargs.pop('work_house', '')
        self.work_postcode = kwargs.pop('work_postcode', '')
        self.work_phone = kwargs.pop('work_phone', '')
        self.mobile_phone = kwargs.pop('mobile_phone', '')
        self.food = kwargs.pop('food', '')
        self.drink = kwargs.pop('drink', '')
        self.music = kwargs.pop('music', '')
        self.status = kwargs.pop('status', '')
        self.online = kwargs.pop('online', 0)

    def __repr__(self):
        return "<Profile('%s'')>" % (self.email)


class ProfileRole(object):
    def __init__(self, **kwargs):
        self.uuid = kwargs.pop('uuid')
        self.role = kwargs.pop('role')

    def __repr__(self):
        return "<ProfileRole('%s'')>" % (self.device_id)


class ProfileSocial(object):

    def __init__(self, **kwargs):
        self.uuid = kwargs.pop('uuid')
        self.service_id = kwargs.pop('service_id')
        self.service_name = kwargs.pop('service_name')
        self.service_url = kwargs.pop('service_url', '')
        self.service_consumer_key = kwargs.pop('service_consumer_key', '')
        self.service_consumer_secret = kwargs.pop(
            'service_consumer_secret', ''
        )
        self.service_access_token = kwargs.pop('service_access_token', '')
        self.service_scope = kwargs.pop('service_scope', '')
        self.service_login = kwargs.pop('service_login', '')
        self.service_email = kwargs.pop('service_email', '')
        self.service_password = kwargs.pop('service_password', '')
        self.notes = kwargs.pop('notes', '')

    def __repr__(self):
        return "<ProfileSocial('%s'')>" % (self.uuid)


class ProfileOtherName(object):

    def __init__(self, **kwargs):
        self.uuid = kwargs.pop('uuid')
        self.name = kwargs.pop('name')

    def __repr__(self):
        return "<ProfileOtherName('%s'')>" % (self.name)


class ProfileRelation(object):
    def __init__(self, **kwargs):
        self.uuid = kwargs.pop('uuid')
        self.type = kwargs.pop('type')
        self.related_account = kwargs.pop('related_account')
        self.related_account_type = kwargs.pop('related_account_type')

    def __repr__(self):
        return "<ProfileSocial('%s'')>" % (self.uuid)


class ProfileEmail(object):

    def __init__(self, **kwargs):
        self.uuid = kwargs.pop('uuid')
        self.email = kwargs.pop('email')

    def __repr__(self):
        return "<ProfileEmail('%s'')>" % (self.email)


class ProfilePicture(object):

    def __init__(self, **kwargs):
        self.uuid = kwargs.pop('uuid')
        self.picture = kwargs.pop('picture')

    def __repr__(self):
        return "<ProfilePicture('%s'')>" % (self.uuid)


class ProfilePhone(object):

    def __init__(self, **kwargs):
        self.uuid = kwargs.pop('uuid')
        self.phone = kwargs.pop('phone')

    def __repr__(self):
        return "<ProfilePhone('%s'')>" % (self.uuid)


class ProfileInterest(object):

    def __init__(self, **kwargs):
        self.uuid = kwargs.pop('uuid')
        self.interest = kwargs.pop('interest')

    def __repr__(self):
        return "<ProfileInterest('%s'')>" % (self.uuid)


class ProfileRequest(object):
    def __init__(self, **kwargs):
        self.uuid = kwargs.pop('uuid')
        self.type = kwargs.pop('type')
        self.request = kwargs.pop('request')

    def __repr__(self):
        return "<ProfileRequest('%s'')>" % (self.uuid)


class ProfileDevice(object):
    def __init__(self, **kwargs):
        self.uuid = kwargs.pop('uuid')
        self.device_id = kwargs.pop('device_id')

    def __repr__(self):
        return "<ProfileDevice('%s'')>" % (self.device_id)


class Device(object):
    def __init__(self, **kwargs):
        self.id = kwargs.pop('id')
        self.device_name = kwargs.pop('device_name')
        self.device_desc = kwargs.pop('device_desc')
        self.device_type = kwargs.pop('device_type')
        self.device_family = kwargs.pop('device_family')
        self.device_model = kwargs.pop('device_model')
        self.device_serial = kwargs.pop('device_serial')
        self.device_make = kwargs.pop('device_make')
        self.device_built = kwargs.pop('device_build')
        self.device_params = kwargs.pop('device_params')
        self.device_location = kwargs.pop('device_location')

    def __repr__(self):
        return "<Device('%s'')>" % (self.device_name)


class ProfileComment(object):
    def __init__(self, **kwargs):
        self.uuid = kwargs.pop('uuid')
        self.comment = kwargs.pop('comment')
        self.area = kwargs.pop('area')

    def __repr__(self):
        return "<ProfileComment('%s'')>" % (self.comment)


class ProfileCronjob(object):
    def __init__(self, **kwargs):
        self.uuid = kwargs.pop('uuid')
        self.job = kwargs.pop('job')

    def __repr__(self):
        return "<ProfileComment('%s'')>" % (self.comment)


class Company(object):

    def __init__(self, **kwargs):
        self.id = kwargs.pop('id')
        self.uuid = kwargs.pop('uuid')
        self.name = kwargs.pop('name', '')
        self.domain = kwargs.pop('domain', '')
        self.type = kwargs.pop('type', '')
        self.registered = kwargs.pop('registered', 0)
        self.founded = kwargs.pop('founded', 0)
        self.updated = kwargs.pop('updated', 0)
        self.homepage = kwargs.pop('homepage', '')
        self.country = kwargs.pop('country', '')
        self.city = kwargs.pop('city', '')
        self.state = kwargs.pop('state', '')
        self.street = kwargs.pop('street', '')
        self.house = kwargs.pop('house', '')
        self.postcode = kwargs.pop('postcode', '')
        self.phone = kwargs.pop('phone', '')
        self.fax = kwargs.pop('fax', '')
        self.location_id = kwargs.pop('house', '')
        self.status = kwargs.pop('status', '')

    def __repr__(self):
        return "<Company('%s'')>" % (self.email)


class CompanyMember(object):

    def __init__(self, **kwargs):
        self.id = kwargs.pop('id')
        self.uuid = kwargs.pop('uuid', '')
        self.company_id = kwargs.pop('company_id', '')
        self.email1 = kwargs.pop('email1', '')
        self.email2 = kwargs.pop('email2', '')
        self.registered = kwargs.pop('registered', 0)
        self.updated = kwargs.pop('updated', 0)
        self.homepage = kwargs.pop('homepage', '')
        self.country = kwargs.pop('country', '')
        self.city = kwargs.pop('city', '')
        self.state = kwargs.pop('state', '')
        self.street = kwargs.pop('street', '')
        self.office = kwargs.pop('office', '')
        self.postcode = kwargs.pop('postcode', '')
        self.cellphone1 = kwargs.pop('cellphone1', '')
        self.cellphone2 = kwargs.pop('cellphone2', '')
        self.cellphone3 = kwargs.pop('cellphone3', '')
        self.phone1 = kwargs.pop('phone1', '')
        self.phone2 = kwargs.pop('phone2', '')
        self.phone3 = kwargs.pop('phone3', '')
        self.fax1 = kwargs.pop('fax1', '')
        self.fax2 = kwargs.pop('fax2', '')
        self.profession = kwargs.pop('profession', '')
        self.info = kwargs.pop('info', '')
        self.location_id = kwargs.pop('house', '')
        self.status = kwargs.pop('status', '')

    def __repr__(self):
        return "<CompanyMember('%s'')>" % (self.uuid)


class ObjectLocation(object):

    def __init__(self, **kwargs):
        self.id = kwargs.pop('id')
        self.obj_id = kwargs.pop('obj_id')
        self.coord = kwargs.pop('coord', '')


class ProfileInteractionHistory(object):

    def __init__(self, **kwargs):
        self.id = kwargs.pop('id')
        self.uuid1 = kwargs.pop('uuid1', '')
        self.uuid2 = kwargs.pop('uuid2', '')
        self.email1 = kwargs.pop('email1', '')
        self.email2 = kwargs.pop('email2', '')
        self.type = kwargs.pop('type', '')
        self.data = kwargs.pop('data', '')
        self.registered = kwargs.pop('registered', 0)
        self.updated = kwargs.pop('updated', 0)

Session = sessionmaker(bind=engine)

#metadata = MetaData(bind=engine, reflect=True)
mapper(Account, account_table)
mapper(Profile, profile_table)
mapper(ProfileRole, profile_role_table)
mapper(ProfileEmail, profile_email_table)
mapper(ProfilePhone, profile_phone_table)
mapper(ProfilePicture, profile_picture_table)
mapper(ProfileSocial, profile_social_table)
mapper(ProfileInterest, profile_interest_table)
mapper(ProfileRequest, profile_request_table)
mapper(ProfileComment, profile_comment_table)
mapper(ProfileRelation, profile_relation_table)
mapper(ProfileOtherName, profile_other_name_table)
mapper(ProfileDevice, profile_device_table)
mapper(ProfileCronjob, profile_cronjob_table)
mapper(ProfileLink, profile_link_table)
mapper(Device, device_table)
mapper(Country, country_table)
mapper(ProfileTimesheet, profile_timesheet_table)
mapper(Company, company_table)
mapper(CompanyMember, company_member_table)
mapper(ProfileInteractionHistory, profile_interaction_table)

metadata.create_all(engine)


def update_list_from_jabber(_dict):
    """docstring for update_list_from_jabber"""
    sess = Session()
    profile = {}

    try:
        for u in _dict:
            profile['email'] = u
            exists = sess.query(Profile).filter(Profile.email == u).all()
            #logger.info('u %s' % type(u))
            #logger.info('u %s' %  u.encode('utf-8'))
            #logger.info('exists %s' % exists)

            if not exists:
                logger.info('Updating %s ' % u)
                us = {}
                us['uuid'] = uuid.uuid4()
                keystring = 'default'
                salt = 'smarty-bot'
                hash = hashlib.md5(salt + keystring).hexdigest()
                us['password'] = hash
                user = Account(**us)
                sess.add(user)
                sess.flush()
                logger.info('uuid: %s saved with id: %s' % (
                    user.uuid, user.id))

                profile['uuid'] = user.uuid
                p = Profile(**profile)
                sess.add(p)

        sess.commit()
    except Exception as e:
        sess.rollback()
        logger.exception(e)


def save_profile_property(uuid, prop, value):
    """docstring for save_property"""
    sess = Session()
    c = sess.query(Profile).filter(Profile.uuid == uuid)
    c.update({prop: value})
    logger.info('profile %s updated with: %s' % (prop, value))
    sess.commit()


def add_profile(profile):
    """docstring for new profile"""
    sess = Session()
    try:

        us = {}
        us['uuid'] = uuid.uuid4()
        keystring = 'default'
        salt = 'smarty-bot'
        hash = hashlib.md5(salt + keystring).hexdigest()
        us['password'] = hash
        user = Account(**us)
        sess.add(user)
        sess.flush()
        logger.info('uuid: %s saved with id: %s' % (user.uuid, user.id))
        profile['uuid'] = user.uuid
        p = Profile(**profile)
        sess.add(p)
        sess.commit()
    except Exception as e:
        sess.rollback()
        logger.exception(e)


def truncate_all(meta):
    """docstring for truncate_all"""
    import contextlib
    #for table in reversed(meta.Base.metadata.sorted_tables):
    #meta.Session.execute(table.delete());
    #meta.Session.commit()
    with contextlib.closing(engine.connect()) as con:
        trans = con.begin()
        for table in reversed(meta.sorted_tables):
            con.execute(table.delete())
            trans.commit()

#truncates fine!
#truncate_all(metadata)
