workers = 2
worker_class = 'socketio.sgunicorn.GeventSocketIOWorker'
bind = '0.0.0.0:8000'
pidfile = '/tmp/gunicorn.pid'
debug = True
loglevel = 'debug'
errorlog = '/tmp/gunicorn.log'
daemon = True
