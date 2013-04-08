# Uros Petrevski, Nodesign.net, WEIO
from tornado import ioloop
from tornado import iostream
import socket
import time
import sys
import json

def send_request():
    
    print "hello"
    for a in range(10) :
        print(str(a))
        time.sleep(1)
        
    stream.close()
    ioloop.IOLoop.instance().stop()

class StdOutputToSocket():
     def write(self, msg):
         out = {}
         out['stdout'] = msg
         stream.write(json.dumps(out))
         
class StdErrToSocket():
    def write(self, msg):
        out = {}
        out['stderr'] = msg
        stream.write(json.dumps(out))


s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM, 0)
stream = iostream.IOStream(s)
stream.connect("uds_weio_main", send_request)

sys.stdout = StdOutputToSocket()
sys.stderr = StdErrToSocket()

ioloop.IOLoop.instance().start()
