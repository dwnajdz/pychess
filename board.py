#! /home/admin/Documents/pychess/chess_env/bin/python
import chess
import chess.svg

# http web server
import os
import http.server
import socketserver
from wsgiref.simple_server import make_server
from wsgiref.validate import validator

class WsgirefServer():
  def __init__(self, port = 3000, static_dir = './static'):
    self.PORT = port
    self.static_dir = static_dir  # Directory where static files are stored

  def http_render_board(self, environ, start_response):
    if environ['PATH_INFO'].startswith('/static/'):
      return self.serve_static(environ, start_response)

    # Open ./index.html file with visual chess board
    _html = open('./index.html', 'r')
    content = _html.read()
    _html.close()

    from io import StringIO
    stdout = StringIO()
    print(content, file=stdout)
    start_response("200 OK", [('Content-Type','text/html; charset=utf-8')])
    return [stdout.getvalue().encode('utf-8')]
  
  def serve_static(self, environ, start_response):
    # Extract the requested file path
    path = environ['PATH_INFO']
    # Construct the full path to the requested file
    file_path = path.lstrip('/')

    if os.path.isfile(file_path):
        with open(file_path, 'rb') as file:
            content = file.read()
        content_type = 'text/javascript' if file_path.endswith('.js') else 'text/css'
        start_response("200 OK", [('Content-Type', content_type)])
        return [content]
    else:
        start_response("404 Not Found", [('Content-Type', 'text/plain')])
        return [b'File Not Found']

  def start(self):
    validator_app = validator(self.http_render_board)
    with make_server('', self.PORT, validator_app) as httpd:
      print("serving on", self.PORT)
      httpd.serve_forever()


server = WsgirefServer(port=3000)
server.start()
