from sys import exit
#from multiprocessing import Process
#from core.config import settings
from core.config.settings import logger
import zmq


class Daemon():
    sock = None
    bsock = None
    response = {}

    def __init__(self, name="undefined"):
        """docstring for __init__"""

        context = zmq.Context()
        self.sock = context.socket(zmq.REP)
        self.sock.bind('ipc:///tmp/smarty-%s' % name)
        #self.sock.connect('ipc:///tmp/smarty-%s' % name)

        #self.bsock = context.socket(zmq.REQ)
        #self.bsock.connect('ipc:///tmp/smarty-brain')
        #self.response = {
            #'text': "error",
            #'jmsg': 'error',
            #'type': 'response'}

    def start(self):
        while True:
            msg = self.sock.recv_json()
            cmd = msg.get('cmd', None)
            if cmd == 'terminate':
                self.response['text'] = 'terminated'
                self.sock.send_json(self.response)
                break
            if cmd:
                response = self.process_command(cmd)
                logger.info('daemon responded with %s' % response)
                self.sock.send_json(response)
        exit()

    def process_command(self, cmd):
        """docstring for process"""
        if cmd == 'run':
            err = 'uhm, I did not understand.'
            try:
                response = self.anymethod()
            except RuntimeError as e:
                logger.exception(e)
                response = {'text': err}
            except OSError as e:
                logger.exception(e)
                response = {'text': err}
            except TypeError as e:
                logger.exception(e)
                response = {'text': err}
            except KeyError as e:
                logger.exception(e)
                response = {'text': err}
            except SyntaxError as e:
                logger.exception(e)
                response = {'text': err}
            except NameError as e:
                logger.exception(e)
                response = {'text': err}
            except AttributeError as e:
                logger.exception(e)
                response = {'text': err}
            except UnicodeEncodeError as e:
                logger.exception(e)
                response = {'text': err}
            except ImportError as e:
                logger.exception(e)
                response = {'text': err}
            except Exception as e:
                logger.exception(e)
                response = {'text': err}
            return response

    def anymethod(self):
        """docstring for run"""
        return 'anymethod method called'


try:
    d = Daemon()
    d.start()
except KeyboardInterrupt:
    logger.info('Terminate process  %s')
    exit()
