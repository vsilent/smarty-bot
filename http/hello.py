from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Smarty is here!'

if __name__ == '__main__':
    http_server = HTTPServer(WSGIContainer(app))
    http_server.listen(80)
    IOLoop.instance().start()
