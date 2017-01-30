import cherrypy

class HelloWorld(object):
    def index(self):
        return "LEL!"
    index.exposed = True

cherrypy.quickstart(HelloWorld())
