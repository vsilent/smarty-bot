#!/usr/bin/env python
# -*- coding: utf-8 -*-
import smtplib
from core.config import settings


def send(msg_from, msg_to, subject, message):

    LOGIN = settings.MY_ACCOUNTS['gmail']['email']
    PASSWORD = settings.MY_ACCOUNTS['gmail']['password']

    msg = ("From: %s\r\nTo: %s\r\nSubject: %s\r\n\r\n"
           % (msg_from, msg_to, subject))
    msg += message + "\r\n"

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.set_debuglevel(1)
    server.ehlo()
    server.starttls()
    server.login(LOGIN, PASSWORD)
    server.sendmail(msg_from, msg_to, msg)
    server.quit()
    return True
