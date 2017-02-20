import cherrypy, os, os.path

class home():
    @cherrypy.expose
    def index(self):
        return open("index.html")

if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__)) + os.path.sep
    config = {
    'global': {
        'environment': 'production',
        'log.screen': True,
        'server.socket_host': '127.0.0.1',
        'server.socket_port': 8080,
        'engine.autoreload_on': True,
        'log.error_file': os.path.join(current_dir, 'errors.log'),
        'log.access_file': os.path.join(current_dir, 'access.log'),
    },
    '/':{
        'tools.staticdir.root' : current_dir,
    },
    '/static':{
        'tools.staticdir.on' : True,
        'tools.staticdir.dir' : 'static',
    },
}
cherrypy.quickstart(home(), '/', config)

