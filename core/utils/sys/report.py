from core.config.settings import MY_ACCOUNTS, PEOPLE
from core.utils.network.email import send


def report_bug(message):
    """docstring for report"""
    send(MY_ACCOUNTS['gmail']['email'], PEOPLE['admin']['email'], 'Smarty-bot bug report', message)
