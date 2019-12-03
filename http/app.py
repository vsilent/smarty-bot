import sys

if 'threading' in sys.modules:
    raise Exception('threading module loaded before patching!')
import gevent.monkey; gevent.monkey.patch_thread()

from threading import Thread
from multiprocessing import Process

import time
from flask import Flask, render_template, session
from flask_socketio import SocketIO, emit
from urllib2 import Request, urlopen, URLError
import logging
from os.path import abspath, dirname
import sys
import zmq
import atexit
from flask import redirect, url_for
from flask_oauth import OAuth

sys.path.append(abspath(dirname(abspath(__file__)) + '../../'))
from core.brain.main import Brain, coolworker
import redis
import pickle

app = Flask(__name__)
app.debug = True
app.config.from_object('config')
app.config['SECRET_KEY'] = 'veryyysecretkeeeeyy!'
socketio = SocketIO(app)
thread = None
oauth = OAuth()

context = zmq.Context()

google = oauth.remote_app(
    'google',
    base_url='https://www.google.com/accounts/',
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    request_token_url=None,
    request_token_params={
        'scope': 'https://www.googleapis.com/auth/userinfo.email',
        'response_type': 'code'
    },
    access_token_url='https://accounts.google.com/o/oauth2/token',
    access_token_method='POST',
    access_token_params={'grant_type': 'authorization_code'},
    consumer_key=app.config['GOOGLE_CLIENT_ID'],
    consumer_secret=app.config['GOOGLE_CLIENT_SECRET']
)


def background_thread(sid):
    """Example of how to send server generated events to clients."""
    count = 0

    def texit():
        sys.exit(0)

    red = redis.Redis(host=app.config['REDIS']['host'])

    while True:
        time.sleep(1)
        # receive output
        res = red.get(sid)
        if not res:
            continue
        red.delete(sid)
        response = pickle.loads(res)
        logging.info('check redis %s session: %s response %s', res, sid, response)
        msg = response.get('html', None)
        if not msg:
            msg = response.get('text', None)
        if msg:
            socketio.emit(
                'my response',
                {'data': msg, 'count': count},
                namespace='/test'
            )


@atexit.register
def goodbye():
    context.term()


@app.route('/')
def index():
    global sender
    session['id'] = int(time.time())

    global thread
    if thread is None:
        thread = Thread(target=background_thread,  args=(session['id'],))
        thread.start()

    return render_template('index.html')


@socketio.on('my event', namespace='/test')
def message(message):
    session['receive_count'] = session.get('receive_count', 0) + 1

    if len(message['data'].strip()) == 0:
        return

    if "connected!" in message['data']:
        emit('my response', {
            'data': 'ready',
            'count': session['receive_count']
        })
        return

    req = {
        'request': message['data'],
        # type of request should be web but smarty
        # is not adapted to accept such
        'from': 'jabber',
        'cmd_path': message['data'].split(),
        'cmd_args': message['data'],
        'sender': '',  # can be set to email
        'uuid': '',  # uuid of local database
        # use session for output socket
        'sid': int(session.get('id'))
    }

    b = Brain()
    try:
        response = b.react_on(req)
    except Exception as e:
        emit(
            'my response', {
                'data': 'sorry, could not process request %s ' % message['data'],
                'count': session['receive_count']
            }
        )
        logging.exception(e)

    # init worker
    w = response.get('worker', None)

    if not isinstance(w, dict):
        return

    logging.info('worker session %s', int(session.get('id')))
    w['sid'] = int(session.get('id'))
    w['cmdaddr'] = 'ipc:///tmp/smarty-worker-input-'
    p = Process(target=coolworker, kwargs=w)
    p.start()
    w['cmdaddr'] = 'ipc:///tmp/smarty-worker-input-%d' % p.pid

    # send command
    context = zmq.Context()
    wis = context.socket(zmq.REQ)
    wis.setsockopt(zmq.LINGER, 100)
    wis.connect(w['cmdaddr'])  # worker input

    # use poll for timeouts:
    poller = zmq.Poller()
    poller.register(wis, zmq.POLLIN)

    wis.send_json({'cmd': 'run'}, zmq.NOBLOCK)

    if poller.poll(5 * 1000):  # 5s timeout in milliseconds
        state = wis.recv_json()
        if state:
            logging.info('worker status %s', state)
    else:
        wis.close()
        context.term()
        emit(
            'my response', {
                'data': 'a bit bussy, please wait .. ',
                'count': session['receive_count']
            }
        )


@socketio.on('connect', namespace='/test')
def connect():
    emit('my response', {'data': 'I am listenning..', 'count': 0})


@socketio.on('disconnect', namespace='/test')
def test_disconnect():
    del session['id']
    logging.info('Client disconnected')


@app.route('/authorize')
def authorize():
    access_token = session.get('access_token')
    if access_token is None:
        return redirect(url_for('login'))

    access_token = access_token[0]

    headers = {'Authorization': 'OAuth ' + access_token}
    req = Request(
        'https://www.googleapis.com/oauth2/v1/userinfo',
        None, headers
    )
    response = None
    try:
        res = urlopen(req)
        response = res.read()
    except URLError as e:
        if e.code == 401:
            # Unauthorized - bad token
            session.pop('access_token', None)
            response = redirect(url_for('login'))
    return response



@app.route('/login')
def login():
    callback = url_for('authorized', _external=True)
    return google.authorize(callback=callback)


@app.route(app.config['REDIRECT_URI'])
@google.authorized_handler
def authorized(resp):
    access_token = resp['access_token']
    session['access_token'] = access_token, ''
    return redirect(url_for('index'))


@google.tokengetter
def get_access_token():
    return session.get('access_token')


if __name__ == '__main__':
    socketio.run(app, host="0.0.0.0", port=80)
