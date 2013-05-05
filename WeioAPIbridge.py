#!/usr/bin/env python
# encoding: utf-8
"""
WeioAPIbridge.py

Created by Uros Petrevski on 2013-05-05.
Copyright (c) 2013 Nodesign.net. All rights reserved.
"""

# -*- coding: utf-8 -*-
import subprocess
import os, signal
import socket
import functools
import errno
import os
from tornado import web, ioloop, iostream

import tornado_subprocess

from sockjs.tornado import SockJSRouter, SockJSConnection
import WeioFiles
import json
import ast

import pickle

p = None

class WeioAPIBridgeHandler(SockJSConnection):
    
    """Opens editor route."""
    def on_open(self, data):
        """On open asks weio for last saved project. List of files are scaned and sent to editor.
        Only contents of weio_main.py is sent at first time"""
        pass
        
        
    def on_message(self, data):
        self.serve(data)
        
    def serve(self, request) :
        pass
