#!/usr/bin/env python3
"""Serve index.html and proxy /api/* → https://api.smartsheet.com/2.0/*"""

import http.server
import urllib.request
import urllib.error
import json
import os

PORT = 8080
SS_BASE = 'https://api.smartsheet.com/2.0'


class Handler(http.server.BaseHTTPRequestHandler):
    def log_message(self, fmt, *args):
        print(f'  {self.command} {self.path} → {args[1]}')

    def send_json(self, code, data):
        body = json.dumps(data).encode()
        self.send_response(code)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(body)

    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Authorization, Content-Type')
        self.end_headers()

    def do_GET(self):
        if self.path.startswith('/api/'):
            self._proxy('GET')
        else:
            self._serve_file()

    def do_POST(self):
        if self.path.startswith('/api/'):
            self._proxy('POST')
        else:
            self.send_json(404, {'error': 'Not found'})

    def _serve_file(self):
        path = 'index.html' if self.path in ('/', '/index.html') else self.path.lstrip('/')
        if not os.path.isfile(path):
            self.send_response(404)
            self.end_headers()
            return
        with open(path, 'rb') as f:
            content = f.read()
        self.send_response(200)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(content)

    def _proxy(self, method):
        ss_path = self.path[len('/api'):]
        url = SS_BASE + ss_path
        auth = self.headers.get('Authorization', '')

        body = None
        if method == 'POST':
            length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(length) if length else None

        req = urllib.request.Request(url, data=body, method=method, headers={
            'Authorization': auth,
            'Content-Type': 'application/json',
        })

        try:
            with urllib.request.urlopen(req) as res:
                data = res.read()
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(data)
        except urllib.error.HTTPError as e:
            data = e.read()
            self.send_response(e.code)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(data)


if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    print(f'Starting server at http://localhost:{PORT}')
    http.server.HTTPServer(('', PORT), Handler).serve_forever()
