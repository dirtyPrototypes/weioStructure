# -*- coding: utf-8 -*-
import os
from tornado import web, ioloop, iostream, options, httpserver
from sockjs.tornado import SockJSRouter, SockJSConnection

# IMPORT EDITOR CLASSES
from editor import Editor #, WeioEditorStopHandler, WeioEditorPlayHandler 

class WeioIndexHandler(web.RequestHandler):
    def get(self):
        self.render('index.html', error="")

class CloseConnection(SockJSConnection):
    def on_open(self, info):
        self.close()

    def on_message(self, msg):
        pass


if __name__ == '__main__':
    import logging
    logging.getLogger().setLevel(logging.DEBUG)

    # EDITOR ROUTES
    WeioEditorRouter = SockJSRouter(Editor.WeioEditorHandler, '/editor/baseFiles')    
    #WeioEditorPlayRouter = SockJSRouter(WeioEditorPlayHandler, '/editor/play')
    #WeioEditorStopRouter = SockJSRouter(WeioEditorStopHandler, '/editor/stop')
    
    #CONFIGURATOR ROUTES


    
    #SETTINGS ROUTES
    
    
    #HELP ROUTE
    
    
    #GENERAL ROUTES
    CloseRouter = SockJSRouter(CloseConnection, '/close')


    app = web.Application(list(WeioEditorRouter.urls) +
                          list(CloseRouter.urls) +
                          [(r"/", WeioIndexHandler),(r"/(.*)", web.StaticFileHandler,
                            					    {"path": "./static", "default_filename": "index.html"})
                          ]
                          )

    options.define("port", default=8081, type=int)
    
    http_server = httpserver.HTTPServer(app)
    http_server.listen(options.options.port)
    
    #app.listen(8081)
    logging.info(" [*] Listening on 0.0.0.0:8081")
    ioloop.IOLoop.instance().start()