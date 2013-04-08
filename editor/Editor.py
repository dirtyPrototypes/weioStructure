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

p = None

class WeioEditorHandler(SockJSConnection):
    
    """Opens editor route."""
    def on_open(self, data):
        """On open asks weio for last saved project. List of files are scaned and sent to editor.
        Only contents of weio_main.py is sent at first time"""
        
        
        
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
               
               processName = './editor/user_weio/weio_main.py'

               #launch process
            
               t = tornado_subprocess.Subprocess(self.on_subprocess_result, args=['python', '-u', processName] )
               t.start()
               
               print("weio_main indipendent process launching...")
               
               # classic blocking method without vukasin tornado-subprocess
               # self.pipe = subprocess.Popen(['python', '-u', processName],
               #                stdout=subprocess.PIPE, stderr=subprocess.PIPE)
               #                ioloop.IOLoop.instance().add_callback(self.on_subprocess_result)
               #                
               #                self.runningState = ioloop.PeriodicCallback(self.checkProcessPlayState, 1000)
               #                self.runningState.start()
               #                
               
           elif 'stop' in rg['request']:
               pipe.kill()
               
               data = {}
               data['serverPush'] = 'stopped'
               
               self.send(json.dumps(data))
               
               
               
    def on_subprocess_result(self, status, stdout, stderr ):
        
        print status, stdout, stderr
        if status == 0:
            print "OK:"
            print stdout
        else:
            print "ERROR:"
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

            
