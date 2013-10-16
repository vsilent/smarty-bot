import logging
import urllib

def info():
    try:
        ip = urllib.urlopen('http://automation.whatismyip.com/n09230945.asp').read()
    except Exception as e:
        logging.exception(e)
        ip = 'Could connect myip service'

    return 'external ip: %s' % ip
