import cherrypy, os, os.path

class host():
    @cherrypy.expose
    def index(self):
        return open("index.html")

if __name__ == "__main__":
    cherrypy.quickstart(host())
