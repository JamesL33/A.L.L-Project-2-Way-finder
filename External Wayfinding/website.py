import cherrypy, os, os.path

class host():
    @cherrypy.expose
    def index(self):
        return open("index2.html")

if __name__ == "__main__":
    cherrypy.quickstart(host())