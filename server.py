#!/usr/bin/env python3
"""Serve index.html, proxy /api/* → Smartsheet, /claude → Anthropic."""

import http.server
import urllib.request
import urllib.error
import os

PORT = 8080
SS_BASE  = 'https://api.smartsheet.com/2.0'
AI_URL   = 'https://api.anthropic.com/v1/messages'


class Handler(http.server.BaseHTTPRequestHandler):
    def log_message(self, fmt, *args):
        print(f'  {self.command} {self.path} → {args[1]}')

    def _cors(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Authorization, Content-Type, X-Api-Key, anthropic-version')

    def do_OPTIONS(self):
        self.send_response(204)
        self._cors()
        self.end_headers()

    def do_GET(self):
        if self.path.startswith('/api/'):
            self._proxy_ss('GET')
        else:
            self._serve_file()

    def do_POST(self):
        if self.path.startswith('/api/'):
            self._proxy_ss('POST')
        elif self.path == '/claude':
            self._proxy_claude()
        else:
            self.send_response(404)
            self.end_headers()

    def _read_body(self):
        length = int(self.headers.get('Content-Length', 0))
        return self.rfile.read(length) if length else None

    def _send(self, code, data, content_type='application/json'):
        self.send_response(code)
        self.send_header('Content-Type', content_type)
        self._cors()
        self.end_headers()
        self.wfile.write(data)

    def _serve_file(self):
        path = 'index.html' if self.path in ('/', '/index.html') else self.path.lstrip('/')
        if not os.path.isfile(path):
            self.send_response(404); self.end_headers(); return
        with open(path, 'rb') as f:
            content = f.read()
        self._send(200, content, 'text/html; charset=utf-8')

    def _proxy_ss(self, method):
        url  = SS_BASE + self.path[len('/api'):]
        auth = self.headers.get('Authorization', '')
        body = self._read_body()
        req  = urllib.request.Request(url, data=body, method=method,
                                      headers={'Authorization': auth, 'Content-Type': 'application/json'})
        try:
            with urllib.request.urlopen(req) as res:
                self._send(200, res.read())
        except urllib.error.HTTPError as e:
            self._send(e.code, e.read())

    def _proxy_claude(self):
        body    = self._read_body()
        api_key = self.headers.get('X-Api-Key', '')
        req     = urllib.request.Request(AI_URL, data=body, method='POST', headers={
            'x-api-key':         api_key,
            'anthropic-version': '2023-06-01',
            'content-type':      'application/json',
        })
        try:
            with urllib.request.urlopen(req) as res:
                self._send(200, res.read())
        except urllib.error.HTTPError as e:
            self._send(e.code, e.read())


if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    print(f'Server running at http://localhost:{PORT}')
    http.server.HTTPServer(('', PORT), Handler).serve_forever()
