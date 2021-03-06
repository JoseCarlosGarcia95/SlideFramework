# -*- coding: utf-8 -*-

# Copyright (c) 2018 José Carlos García (hola@josecarlos.me)
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
from http.server import BaseHTTPRequestHandler, HTTPServer
from os import curdir, sep, path
from .framework import SlideFramework
import mimetypes

import json
class SlideFrameworkHandler(BaseHTTPRequestHandler):
    def __init__(self, *args):
        mimetypes.init()

        self.handlers = {}
        
        self.handlers[''] = self.loadIndex
        
        self.handlers['static'] = self.loadStatics
        self.handlers['config.json'] = self.loadConfig
        self.handlers['my-presentation'] = self.loadMyPresentation
        self.handlers['my-modules'] = self.loadMyModules

        BaseHTTPRequestHandler.__init__(self, *args)
      
    def loadIndex(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        
        self.wfile.write(SlideFramework.indexresponse())

    def loadConfig(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json; charset=utf-8')
        self.end_headers()
        
        self.wfile.write(str.encode(json.dumps(SlideFramework.slidesconfig)))

    def loadMyModules(self):
        query_args = self.path.split('/')

        if len(query_args) < 2:
            return
        
        handler    = query_args[2]

        if not handler in SlideFramework.modules.keys():
            return

        func = SlideFramework.modules[handler]
        func(self)
        
    def loadMyPresentation(self):
        query_args = self.path.split('/')
        del query_args[1]

        self.path = path.sep.join(query_args)

        realpath = path.sep.join([SlideFramework.slidesdir, self.path])
        name, ext = path.splitext(self.path)

        mimetypes.types_map['woff'] = 'application/x-font-woff'
        mimetypes.types_map['woff2'] = 'application/x-font-woff'
            
        if ext in mimetypes.types_map:
            mimetype = mimetypes.types_map[ext]
        else:
            mimetype = "text/plain"

        self.send_response(200)
        self.send_header('Content-type', mimetype)
        self.end_headers()
        
        staticfile = open(realpath, 'rb')
        self.wfile.write(staticfile.read())
        staticfile.close()
        
    def loadStatics(self):
        realpath = path.sep.join([path.dirname(path.abspath(__file__)), "..", self.path])
        name, ext = path.splitext(self.path)

        mimetypes.types_map['woff'] = 'application/x-font-woff'
        mimetypes.types_map['woff2'] = 'application/x-font-woff'
            
        if ext in mimetypes.types_map:
            mimetype = mimetypes.types_map[ext]
        else:
            mimetype = "text/plain"

        self.send_response(200)
        self.send_header('Content-type', mimetype)
        self.end_headers()
        
        staticfile = open(realpath, 'rb')
        self.wfile.write(staticfile.read())
        staticfile.close()

    def do_GET(self):
        if "/../" in self.path:
            return
        
        query_args = self.path.split('/')
        handler    = query_args[1]

        if handler in self.handlers.keys():
            self.handlers[handler]()

def createhttpserver(port, template, slides):
    # Initialize SlideFramework.
    SlideFramework.startengine(template, slides)

    # Starts listening connections.
    server = HTTPServer(('', port), SlideFrameworkHandler)
    print('Started httpserver on port http://127.0.0.1:{}'.format(port))
    
    # Wait forever for incoming htto requests
    server.serve_forever()
