#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cmd
import sys
from multiprocessing import Process
from os.path import abspath, dirname
sys.path.append(abspath(dirname(abspath(__file__)) + '../../../'))
from core.brain.main import Brain, worker
from core.config.settings import PEOPLE
import zmq


class Shell(cmd.Cmd):
    """Simple command processor example."""

    prompt = 'smarty-bot > '

    def do_prompt(self, line):
        "Change the interactive prompt"
        self.prompt = line + '> '

    def default(self, req):
        """docstring for default"""

        context = zmq.Context()
        request = {
            'request': req,
            'from': 'jabber',
            'cmd_path': req.split(),
            'cmd_args': req,
            'sender': PEOPLE['admin']['email'],
            'uuid': ''
        }
        b = Brain()
        response = b.react_on(request)

        ##check workers activity
        w = response.get('worker', None)
        if w:
            w['addr'] = 'ipc:///tmp/smarty-brain-worker-'
            p = Process(target=worker, kwargs=w)
            p.start()
            w['addr'] = 'ipc:///tmp/smarty-brain-worker-%d' % p.pid
            ws = context.socket(zmq.REQ)
            ws.connect(w['addr'])
            ws.send_json({'cmd': 'run'})
            response = ws.recv_json()
            if response:
                print(response['text'])
                #cont = response.get('continue', '')
                ws.send_json({'cmd': 'terminate'})
                ws.close()
                p.terminate()
            else:
                print(response['text'])

    def do_EOF(self, line):
        return True

if __name__ == '__main__':
    Shell().cmdloop()
