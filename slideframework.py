#!/usr/bin/python3
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

import argparse
from slideframework import HTTPsimple

# Start the program.
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Start the backend for SlideFramework')

    # Parse arguments.
    parser.add_argument('--port', default=8080, help='HTTP Server port', type=int)
    parser.add_argument('--template', default='default', help='Specify a template')
    parser.add_argument('--slides', default='', help='Your slides')
    
    args   = parser.parse_args()

    # Start listening connections.
    HTTPsimple.createhttpserver(args.port, args.template, args.slides)
