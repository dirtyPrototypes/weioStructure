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

class WeioEditorHandler(SockJSConnection):
    
    """Opens editor route."""
    def on_open(self, data):
        """On open asks weio for last saved project. List of files are scaned and sent to editor.
        Only contents of weio_main.py is sent at first time"""
        pass
        
        
    def on_message(self, data):
        self.serve(data)
        
        
    def serve(self, request) :
           
           rq = ast.literal_eval(request)
           
        
           data = {}
           #print(rq)
           
           if 'getFileList' in rq['request'] :
               
               # echo given request
               data['requested'] = rq['request']
               
               # read all files paths from user directories
               data['data'] = WeioFiles.scanFolders()
               
               fileList = data 
               
               #sending
               self.send(json.dumps(data))
               #print('server sends...', json.dumps(data))
               
           elif 'getFile' in rq['request'] :

               # echo given request
               data['requested'] = rq['request']

               # echo given data
               data['requestedData'] = rq['data']

               fileInfo = rq['data']

               pathname = fileInfo['path']

               rawFile = WeioFiles.getRawContentFromFile(pathname)

               fileInfo['data'] = rawFile

               data['data'] = fileInfo
               self.send(json.dumps(data))
            
           elif 'saveFile' in rq['request']:

               # echo given request
               data['requested'] = rq['request']

               # don't echo given data to spare unnecessary communication, just return name 
               fileInfo = rq['data']
               data['requestedData'] = fileInfo['name']

               pathname = fileInfo['path']
               rawData = fileInfo['data']
               
               #print(pathname + " " + rawData)
               ret = WeioFiles.saveRawContentToFile(pathname, rawData)
  
               self.send(json.dumps(data))
               
           elif 'play' in rq['request']:
               
               processName = './static/user_weio/weio_main.py'

               #launch process
            
               weio_main = tornado_subprocess.Subprocess(self.on_subprocess_result, args=['python', processName])
               weio_main.start()
               
               print("weio_main indipendent process launching...")
               
               # classic blocking method without vukasin tornado-subprocess
               # self.pipe = subprocess.Popen(['python', '-u', processName],
               #                stdout=subprocess.PIPE, stderr=subprocess.PIPE)
               #                ioloop.IOLoop.instance().add_callback(self.on_subprocess_result)
               #                
               #                self.runningState = ioloop.PeriodicCallback(self.checkProcessPlayState, 1000)
               #                self.runningState.start()
               #                
               
               #####################################
               # open UNIX DOMAIN SOCKET
               #####################################
               
               # TODO pass type of socket in constructor
               sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM, 0)
               sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
               sock.setblocking(0)
               server_address = "uds_weio_main"

               # Make sure the socket does not already exist
               try:
                   os.unlink(server_address)
               except OSError:
                   if os.path.exists(server_address):
                       raise

               sock.bind(server_address)
               # how many connections I can accept
               sock.listen(10)
               
               ioloopObj = ioloop.IOLoop.instance()
               
               callback = functools.partial(self.socket_connection_ready, sock)
               ioloopObj.add_handler(sock.fileno(), callback, ioloopObj.READ)
               
           elif 'stop' in rg['request']:
               weio_main.stop()
               data = {}
               data['serverPush'] = 'stopped'
               
               self.send(json.dumps(data))
               
               
    def socket_connection_ready(self, sock, fd, events):
       global stream


       print "CONNECTION READY"
       while True:
           print "AAA"
           try:
               connection, address = sock.accept()
               print "client connected to UNIX domain socket"
           except socket.error, e:
               print "HERE"
               if e[0] not in (errno.EWOULDBLOCK, errno.EAGAIN):
                   raise
               return
           connection.setblocking(0)
           global stream
           stream = iostream.IOStream(connection)
          
           stream.read_until_close(self.socket_on_close, self.socket_on_headers)
          
           
    def socket_on_headers(self, data):
       print "-> ENTER on_headers()"
       
       rcvd = pickle.loads(data)
       print rcvd
       
       self.sendToBrowser(rcvd)
  
       #global stream
       #stream.write("OK, zatvori Mile...")
       #stream.read_until("\t", on_close)
       print "<- EXIT on_headers()"

    def socket_on_close(self, data):
       # here error happens and socket will be closed
       
       print "-> ENTER on_close()"
       
       rcvd = pickle.loads(data)
       
       #print "LLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLL"
       #print rcvd
       #print "EEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE"
        
       err = {}
       err['stderr'] = rcvd['stdout']
       
       self.sendToBrowser(err)
           
       global stream
       stream.close()
       print "closed socket"
       print "<- EXIT on_close()"
       
    def sendToBrowser(self, rcvd) :
      # pack and send to client
      
       data = {}

       if 'stdout' in rcvd :
           data['serverPush'] = 'stdout'
           data['data'] = rcvd['stdout']
       elif 'stderr' in rcvd :
           data['serverPush'] = 'stderr'
           data['data'] = rcvd['stderr']

       self.send(json.dumps(data))
           
    def on_subprocess_result(self, status, stdout, stderr, has_timed_out ):
        
        print status, stdout, stderr
        if status == 0:
            print "OK:"
            print stdout
        else:
            print "ERROR:"
            print stdout
            print stderr
                
                # 
                # data  = {}
                # 
                # global errorBuffer
                # 
                # errInFile = ""
                # errInLine = ""
                # 
                # line = self.pipe.stdout.readline()
                # err = self.pipe.stderr.readline()
                # 
                # if line :
                #     print line
                #     
                #     # pack and send to client
                #     data['serverPush'] = 'stdout'
                #     data['data'] = line
                #     self.send(json.dumps(data))
                #     
                #     ioloop.IOLoop.instance().add_callback(self.on_subprocess_result)
                #     
                # if err :
                #     
                #     if 'Traceback (most recent call last):' in err :
                #         print "traceback info is comming"
                #         errorBuffer = err
                # 
                #         
                #     elif  'File "' in err :
                #         arg = err.split(",")
                #         errInFile = arg[0].split('"')
                #         errInFile = errInFile[1]
                #         
                #         #print errInFile
                #         
                #         errInLine = arg[1].split("line")
                #         errInLine = errInLine[1]
                #         
                #         errorBuffer = errorBuffer + err
                #         print errInLine
                #     elif 'NameError:' in err :
                #         #last message
                #         errorBuffer = errorBuffer + err
                #        
                #         # pack and send error to client
                #         data['serverPush'] = 'stderr'
                #         data['data'] = errorBuffer
                #         data['errorInFile'] = errInFile
                #         data['errorInLine'] = errInLine
                #         
                #         self.send(json.dumps(data))
                #        
                #         if (self.pipe.poll()==1) :
                #             # process has been terminated due to an error
                #             # inform client
                #             data = {}
                #             data['serverPush'] = 'stopped'
                #             
                #             self.send(json.dumps(data))
                #         
                #     ioloop.IOLoop.instance().add_callback(self.on_subprocess_result)
    
    def checkProcessPlayState(self) :
        #print(str(self.pipe.poll()))
        if (self.pipe.poll()==0) :
            print("yupiiii")
            data = {}
            data['serverPush'] = 'stopped'
        
            self.send(json.dumps(data))