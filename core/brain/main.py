#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Primitive Brain :)

"""
import sys
import os
import zmq
import imp
from core.utils.utils import Utils
from unipath import Path
from core.config import settings
from core.config.settings import logger, ROBOT_DIR
from core.lib.wikipedia.search import search
from core.lib.wikipedia.wiki import Wiki
import re
import resource
import subprocess
from core.recognize import recognize_by_google
from core.listen import listen, reset_input
from broadcast import say
from core.people.requests import save_users_request


def worker(**kwargs):
    sys.stdout.flush()
    addr = kwargs.get('addr', None)
    addr += str(os.getpid())
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind(addr)
    cmd_path = kwargs.get('cmd_path', '')
    fn = ROBOT_DIR.child('core', 'brain') + \
        '/' + '/'.join(cmd_path) + '/reaction.py'

    try:
        rmod = Brain.load_from_file(fn)
    except IOError as e:
        msg = socket.recv_json()
        response = {'text': 'uhm, I did not understand'}
        e.message = e.message + 'tryed to load %s' % fn
        logger.exception(e)
        #ZMQError
        try:
            socket.send_json(response)
        except Exception as e:
            pass
        exit()
    except Exception as e:
        msg = socket.recv_json()
        response = {'text': 'uhm, I did not understand'}
        e.message = e.message + 'tryed to load %s' % fn
        logger.exception(e)
        #ZMQError
        try:
            socket.send_json(response)
        except Exception as e:
            pass
        exit()

    try:
        react = rmod.Reaction('reserved', *{'arg': 'reserved'}, **kwargs)
    except Exception as e:
        msg = socket.recv_json()
        response = {'text': 'uhm, I did not understand'}
        logger.exception(e)
        #ZMQError
        try:
            socket.send_json(response)
            exit()
        except Exception as e:
            pass
        exit()

    #run worker server
    while True:
        msg = socket.recv_json()
        cmd = msg.get('cmd', None)

        if cmd == 'run':
            err = 'uhm, I did not understand.'
            try:
                response = react.run()
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

            logger.info('%s responded with %s' % (rmod, response))

        if cmd == 'on_continue':
            try:
                response = react.on_continue(msg)
            except Exception as e:
                logger.exception(e)
                response = {'text': err}

        if cmd == 'terminate':
            socket.send_json(response)
            break

        socket.send_json(response)

    exit()


class Brain():
    """class Brain"""

    req_obj = {}
    request = ''
    response = {}
    _dialog_stage = None
    _request_processed = False
    _continue_dialog = False
    _is_question = False
    _is_greeting = False
    _is_command = False
    _cmd_args = []
    _cmd_path = []
    _response = None
    cmd_stack = []
    _initiator = None
    _utils = Utils()
    sockets = {'output': '', 'worker': '', 'master': ''}
    workers = []

    def __call__(self):
        pass

    def __str__(self):
        return 'Brain'

    def __init__(self, initiator=None):

        #is not active by default
        self.set_dialog_stage(0)
        self._initiator = initiator
        self.pid = os.getpid()
        self.context = zmq.Context()

        self.sockets['output'] = self.context.socket(zmq.PUB)
        self.sockets['output'].bind('ipc:///tmp/smarty-output')

        self.sockets['master'] = self.context.socket(zmq.REP)
        self.sockets['master'].connect('ipc:///tmp/smarty-brain-master-%d'
                                       % self.pid)

        self.sockets['worker'] = self.context.socket(zmq.REQ)
        self.sockets['worker'].connect('ipc:///tmp/smarty-brain-worker-%d'
                                       % self.pid)

    @staticmethod
    def setlimits():
        # Set maximum CPU time to 1 second in child process,
        # after fork() but before exec()
        logger.info("Setting resource limit in child(pid %d)" % os.getpid())
        resource.setrlimit(resource.RLIMIT_CPU, (0.1, 0.1))

    @classmethod
    def output(self, req_obj):
        """docstring for outp"""
        self.sock['output'].send_json(req_obj)

    @classmethod
    def set_dialog_stage(self, stage):
        """docstring for set dialog stage"""
        self._dialog_stage = stage

    @classmethod
    def get_dialog_stage(self):
        """ Return dialog stage """
        return int(self._dialog_stage)

    @classmethod
    def set_request_as_unknown(self):
        """ set request attribute as unknown"""
        self._is_greeting = False
        self._is_command = False
        self._is_question = False
        self._request_processed = False

    @classmethod
    def set_request_as_question(self):
        """ set request as question """
        self._is_greeting = False
        self._is_command = False
        self._is_question = True
        self._request_processed = False

    @classmethod
    def set_request_as_greeting(self):
        """ set request as greeting """
        self._is_greeting = True
        self._is_command = False
        self._is_question = False
        self._request_processed = False

    @classmethod
    def set_request_as_command(self):
        """ set request as command """
        self._is_greeting = False
        self._is_command = True
        self._is_question = False
        self._request_processed = False

    #return request
    @classmethod
    def react_on(self, req_obj):
        """
        split requested sentense by space
        greetings must be a tuple
        """
        logger.info('Brain.react_on() got: %s of type %s'
                    % (req_obj, type(req_obj)))

        self.req_obj = req_obj
        req_type = self.req_obj.get('type', '')

        #todo
        #if request object already include request type like is_question
        #then skip request parsing and execute method directly
        req_types = ['is_question', 'is_command', 'is_greeting']

        if req_type in req_types:
            #return eval(req_type, {"__builtins__":None})
            if 'is_question' == req_type:
                return self.is_question(req_obj['request'])
            if 'is_command' == req_type:
                return self.is_command(req_obj['request'])

        request = req_obj.get('request', None)

        self._initiator = req_obj.get('from', None)
        self.set_request_as_unknown()

        if request is None:
            logger.info('empty request')
            return {'error': 'empty request'}

        request = request.strip()

        #are polite words in request ? cut them
        request = self.remove_polite_words(request)

        #Noise is usually recognized as "no no no no" text
        #try to cut it from start and end
        if self._initiator == 'julius':
            request = self.remove_possible_noise_words(request)
            logger.info('sentense after cutting noise words: %s', request)

        self.request = request

        #-------------------------------------------------------------->
        #try to recognize name and simple answers like "yes"
        #"no" by local application
        #dialog not started, wait for greeting or name

        if self.get_dialog_stage() == 0 and self._initiator == 'julius':
            if request.startswith(settings.MY_NAME) or \
               request.startswith(settings.GREETINGS):
                self.set_dialog_stage(1)
                pass
            else:
                return {'type': 'response', 'text': '', 'say': '', 'fake': 1}

        if self.get_dialog_stage() == 1 and self._initiator == 'julius':
            while 1:
                logger.info('Listen again ... break and restart dialog \
                            in case of inactivity in 10 seconds')
                speech_recorded = False
                try:
                    logger.info('Recording speech...')
                    listen()
                    speech_recorded = True
                except RuntimeError as e:
                    say('Any Questions?')
                    reset_input()
                    speech_recorded = False

                if not speech_recorded:
                    try:
                        logger.info('Recording speech, second attempt...')
                        listen()
                    except RuntimeError as e:
                        self.finish_dialog()
                        break

                logger.info("Stage after recording speech: %d",
                            self.get_dialog_stage())

                request_received = False

                try:
                    request_received = recognize_by_google()
                    logger.info("Stage: %d",
                                self.get_dialog_stage())
                    logger.info("Reaction processed: %d",
                                self._request_processed)
                    logger.info("Is greeting: %d",
                                self._is_greeting)
                    logger.info("Rest of sentense: %s",
                                request_received)
                except RuntimeError as e:
                    self.error(e)

                if request_received:
                    #first request can be greeting with answer in one file
                    #result can be None or the rest part of
                    #first request(greeings from beggining cut)
                    rest = self.react_on(request_received)
                    logger.info("After robot's reaction")
                    logger.info("Stage: %d",
                                self.get_dialog_stage())
                    logger.info("Reaction processed: %d",
                                self._request_processed)
                    logger.info("Is greeting: %d",
                                self._is_greeting)
                    logger.info("Rest of sentense: %s",
                                rest)

                    if self.get_dialog_stage() == 0:
                        logger.info("Skip dialog... restart")
                        break
        #------------------------------------------>

        if len(request) == 0:
            self.set_request_as_greeting()
            return '?'

        if self.is_a_command(request):
            self.set_request_as_command()
            self.cmd_stack.append(request)
            return self.is_command(req_obj)

        elif self.is_a_question(request):
            logger.info('Sentense is a question!')

            if request.endswith('?'):
                request = request[:-1]

            self.set_request_as_question()
            #look if there are no reaction modules or commands by this question
            #continue search in internet or local database
            return self.is_question(request)

        #if not recognized than try to search it by google
        #and get apropriate suggestion information
        elif self.get_dialog_stage() == 1:
            #logger.info('Sentense was not recognized,
            #please try to repeat your question')
            self.set_dialog_stage(1)
            self.set_request_as_greeting()
            return self.is_question(request)
        #if this is more then greeting
        else:
            sender = self.req_obj.get('sender', '')
            #@todo data-sort-bot check the heap of requests, what is it, if an email whose and sort it ?
            save_users_request(sender, request)
            self.response = {'text': 'got it.'}

            #@todo ascii request
            try:
                request.decode('ascii')
            except UnicodeDecodeError as e:
                logger.info("it was not a ascii-encoded unicode string")
                self.response = {'text': str(e)}
            else:
                logger.info("It may have been an ascii-encoded unicode string")

            self.set_dialog_stage(0)
            return self.response

    @classmethod
    def is_greeting(self, request):
        logger.info(' function is not ready ')
        pass

    @classmethod
    def is_a_command(self, request):
        """
        is the request a command ?
        trying to recognize a command
        and keep command and args to avoid double parsing

        """
        request = request.lower()
        if request.endswith('?'):
            request = request[:-1]

        is_command = False
        #@todo meet a problem when command has two or more words,
        #need to check this also
        command_list = request.split()

        path = Path(
            ROBOT_DIR.child('core', 'brain') + '/'
            + '/'.join(request.split()) + '/reaction.py')

        if not is_command and len(command_list) > 1:
            logger.info('Command %s consist of %d words' % (
                request, len(command_list)))
            self._cmd_args = command_list
            self._cmd_path = []

            #this method will try to find first full cmd
            # after that one level up
            if path.isfile():
                is_command = True
                logger.info('Reaction file has been found at %s', self._cmd_path)
                logger.info('Request is command .. continue')
                # set something like  ['ping', 'my', 'sites']
                #self._cmd_path = path.relative().parent.split('/')
                self._cmd_path = self._cmd_args

        #last added
        #user defined script
        if path.isfile() and not is_command:
            logger.info('User defined reaction found at %s', path)
            is_command = True
            # sets something like  ['ping', 'my', 'sites']
            #self._cmd_path = path.relative().parent.split('/')
            self._cmd_path = command_list
            self._cmd_args = command_list
            logger.info('cmd_path %s', self._cmd_path)
        #
        #  First check for simple(one word) commands
        #  why ?
        #  moved to second position
        #  example :  I want to know : who is looking for a thing in internet
        # instead of who is Chuck Norris
        if is_command is False:
            logger.info('Check for embedded..')
            if request.startswith(settings.EMBEDDED_COMMANDS):
                logger.info('Embedded command detected %s!' % self._cmd_path)
                for c in settings.EMBEDDED_COMMANDS:
                    if request.startswith(c):
                        break
                self._cmd_path = c.split()
                self._cmd_args = request.replace(c, '').split()
                is_command = True

        if is_command is False:
            self._request_processed = False
            self._continue_dialog = True
            logger.info('Request is not a command .. continue')

        return is_command

    @classmethod
    def proceed_on_reaction(self, request, req_obj):
        """
            #================= extended commands section =============
        """
        path = self._utils.get_full_path_to_module_by_request(request)
        #else parse words in first request  and try to find a reaction module

        #do not copy default module without confirming
        if not os.path.isfile(path + '/reaction.py') and \
           not self._continue_dialog:
            self._request_processed = False
            self._continue_dialog = True
            return request
        elif(os.path.isfile(path + '/reaction.py')):
            w = {}
            w['req_obj'] = req_obj
            w['cmd_path'] = self._cmd_path
            w['cmd_args'] = self._cmd_args
            w['cmd_stack'] = self.cmd_stack
            logger.info('is_command() worker %s ' % w)
            return {'type': 'response', 'worker': w}
        return self.response

    @classmethod
    def continue_analisys(self, request):
        """docstring for continue_analisys"""
        return request

    @staticmethod
    def load_from_file(filepath):
        """
            find path
        """
        expected_class = 'Reaction'
        mod_name, file_ext = os.path.splitext(os.path.split(filepath)[-1])
        logger.debug(filepath)
        logger.debug(mod_name)

        if file_ext.lower() == '.py':
            try:
                py_mod = imp.load_source(mod_name, filepath)
            except Exception as e:
                logger.exception(e)
                raise e
        elif file_ext.lower() == '.pyc':
            py_mod = imp.load_compiled(mod_name, filepath)
        if expected_class in dir(py_mod):
            return py_mod

    @classmethod
    def is_a_question(self, request):
        request = request.lower()
        """check if request is_a_question"""
        if request.startswith(settings.S_QUESTIONS):
            return True
        if request.endswith(settings.E_QUESTIONS):
            return True
        if request.endswith('?'):
            return True
        return False

    @classmethod
    def remove_polite_words(self, request):
        """docstring for remove_polite_words"""
        for word in settings.POLITE:
            if word in request:
                request = request.replace(word, '')
        return request

    @classmethod
    def remove_possible_noise_words(self, text):
        """Sometimes noise recognized as 'no' words or "#"
        symbols ( speech recognition),
        we will try to find them and remove"""
        if text.startswith('no '):
            text = re.search('^[no\s]+(.+)$', text)
            text = text.group(1)
        if text.startswith('saw '):
            text = re.search('^saw\s(.+)$', text)
            text = text.group(1)
        if text.endswith(' no'):
            text = re.search('(.+)[\sno\s]+$', text)
            text = text.group(0)
        if "#" in text:
            text = text.replace('#', '')
        return text

    @classmethod
    def is_command(self, req_obj):
        """prepare worker for a command"""
        w = {}
        w['req_obj'] = req_obj
        w['cmd_path'] = self._cmd_path
        w['cmd_args'] = self._cmd_args
        w['cmd_stack'] = self.cmd_stack
        #self.workers.append(w)
        logger.info('is_command() worker %s ' % w)
        return {'type': 'response', 'worker': w}

    @classmethod
    def sock_response(self, _obj):
        """docstring for listen_worker"""
        context = zmq.Context()
        socket = context.socket(zmq.REP)
        socket.bind(_obj.get('addr'))
        while True:
            #listen to worker
            response = socket.recv_json()
            if response:
                if response.get('continue') == 1 and \
                   response.get('type') != '':
                    self.attempt += 1
                    logger.info('attempt %d' % self.attempt)
                    if self.attempt > 5:
                        logger.info('attempt %d' % self.attempt)
                        break
                    self.react_on(response)
                return response
        return {"text": "sorry, don't understand question",
                "jmsg": "sorry, don't understand question"}

    @classmethod
    def is_question(self, text):
        """
        Noise is usually recognized as "no no no no"
        text try to cut it from start and end
        check if question not empty after cutting polite words
        """
        #logger.info("Got a new question: %s" % text)
        if len(text) == 0:
            if self._initiator == 'julius':
                self.response = {
                    'say': "DON'T UNDERSTAND, PLEASE REPEAT YOUR QUESTION",
                    'continue': 1}
                self.set_dialog_stage(1)
                return self.response
            else:
                self.response = {
                    'text': "DON'T UNDERSTAND, PLEASE REPEAT YOUR QUESTION",
                    'continue': 1}
                return self.response

        if self._initiator == 'julius':
            text = self.remove_possible_noise_words(text)

        logger.info('question after cleanup: %s' % text)
        state = 0

        # Is this a new question ?
        if state == 0 or (state is None):

            logger.info("I don't know, going to search dictionary!")
            link_to_audio = self.search_www_for_audio(text)

            downloaded = False

            if link_to_audio:
                downloaded = self._utils.download_audio_resource(
                    link_to_audio,
                    text)
                if downloaded:
                    self.response = {'text': text}
                else:
                    logger.info("No media found")

            #should be a plugin
            #answer = self.askBigDb(text)
            #if answer:
                #self.response['text'] = answer
                #self.response['jmsg'] = answer
                #self.response['type'] = 'response'
                #self.response['continue'] = 0
                #return self.response

            ##but first split text by question part
            for q in settings.S_QUESTIONS:
                text = text.replace(q, '').strip()
            #@todo split words and check one by one
            logger.info('check %s in dictionary' % text)
            resp = self.find_by_linux_dict(text)

            if resp:
                self.response['text'] = resp
                self.response['jmsg'] = resp
                self.response['type'] = 'response'
                self.response['continue'] = 0
            else:
                logger.info('nothing in dictionary, searching internet...')
                self.response['text'] = self.search_www(text) or \
                    'sorry, no idea.. search function is not ready'
                self.response['jmsg'] = self.search_www(text) or \
                    'sorry, no idea.. search function is not ready'
                self.response['type'] = 'response'
                self.response['continue'] = 0

            return self.response
        else:
            #already know the answer:) play it
            self.response = {'text': text, 'play': text}

        if self._initiator == 'julius':
            #remove all recorded questions
            subprocess.Popen(
                ["rm", '-f',
                 settings.APP_DIRS['tmp_input_audio_dir'] + '*.wav ']
            )

        self.finish_dialog()
        return self.response

    @classmethod
    def askBigDb(self, text):
        """askBigDb http://thebigdb.com/"""
        return text
        #from core.lib.thebigdb.thebigdb import TheBigDB
        #thebigdb = TheBigDB()
        #r = thebigdb.search([text])
        #return " ".join(r.nodes)

    @classmethod
    def finish_dialog(self):
        """
        finish dialog, reset all attributes
        """
        self.set_dialog_stage(0)
        self._request_processed = False
        self._continue_dialog = False
        self._is_question = False
        self._is_greeting = False
        #logger.info('Dialog finished.')

    @classmethod
    def search_www(self, q):
        """@todo this functionality should be splitted
        to plugins and multiprocessed"""
        pass

    @classmethod
    def search_www_for_audio(self, text_to_search):
        """docstring for search_www"""
        #small hack for searching exactly wiki or dictionary files
        json_results = search(text_to_search)
        # now grep the results and find wiki info
        if not json_results:
            say('OOPS, COULD NOT CONNECT GOOGLE')
            return False

        _wiki = Wiki()
        wiki_page_link = _wiki.find_resourse_link(json_results)

        if wiki_page_link:
            link_to_audio = _wiki.find_audio_resourse(wiki_page_link)

            info = {'audio_external': link_to_audio,
                    'wiki_external': wiki_page_link,
                    'audio_local': ''}
            self._utils.save_file_json_info(text_to_search, info)

            if link_to_audio:
                return link_to_audio

        return False

    @classmethod
    def find_by_linux_dict(self, text):
        """docstring for found_by_linux_dict"""

        logger.info('find definition using local linux dict... %s', text)
        proc = subprocess.Popen(
            ["/usr/bin/dict", text],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=False)
        txt = ''

        for line in proc.stdout.readlines():
            txt += line.replace('\n', "\n")
        return txt

    @classmethod
    def suggest_info(self, text):
        """ suggest way to get info """
        return text

    @classmethod
    def error(self, error):
        """ say about error """
        self.response = {'error': error, 'text': error}
        self.set_dialog_stage(0)
        return self.response

    @classmethod
    def create_new_reaction(self, text):
        """docstring for create_new_reaction"""
        path = self._utils.get_full_path_to_module_by_request(text)
        #make a copy of default reaction files
        if not os.path.isfile(path + '/reaction.py'):
            self._utils.copy_default_reaction_files(path + '/')

    @classmethod
    def exec_comm_subprocess(self):
        """docstring for exec_comm_subprocess"""
        logger.info("CPU limit of parent(pid %d)" % os.getpid(),
                    resource.getrlimit(resource.RLIMIT_CPU))
        rmod = self.load_from_file(
            settings.APP_DIRS['brain_modules_dir'] +
            '/'.join(self._cmd_path) + '/reaction.py')
        logger.info('Open subprocess for %s' % rmod)
        p = subprocess.Popen(
            ["python", rmod],
            preexec_fn=self.setlimits
        )
        logger.info("CPU limit of parent(pid %d) after startup of child" % os.getpid(),
                    resource.getrlimit(resource.RLIMIT_CPU))
        p.wait()
        logger.info("CPU limit of parent(pid %d) after child finished executing" % os.getpid(),
                    resource.getrlimit(resource.RLIMIT_CPU))
