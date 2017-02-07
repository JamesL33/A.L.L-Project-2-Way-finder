import cherrypy, os, os.path

class home():
    @cherrypy.expose
    def index(self):
        return open("index.html")

if __name__ == "__main__":
	cherrypy.tree.mount(home(), "/", "website.conf")
	cherrypy.engine.start()
