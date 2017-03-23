import cherrypy
import os
import os.path
import security
import Dijkstra
import dominate
from dominate.tags import *


class home():

    @cherrypy.expose
    def index(self):
        return open("index.html")

    @cherrypy.expose
    def campusNav(self):
        return open("campusNav.html")

    @cherrypy.expose
    def covUniBuildings(self):
        return open("covUniBuildings.html")

    @cherrypy.expose
    def ecBuildingNav(self):
        return open("ecBuildingNav.html")

    @cherrypy.expose
    def about(self):
        return open("about.html")

    @cherrypy.expose
    def campusMap(self):
        return open("campusMap.html")

    @cherrypy.expose
    def admin(self, username=None, userpassword=None):
        if cherrypy.session.get('loggedon'):
            return open("about.html")
        if username is None or userpassword is None:
            return open("admin.html")
        with security.Security() as password_check:
            try:
                password_check.log_on(username, userpassword)
                # replace with successful page
                cherrypy.session["loggedon"] = True
                return open("about.html")
            except ValueError:
                # replace with unsuccessful page
                return open("adminFailLogin.html")

    @cherrypy.expose
    # todo: Make start and end be passed by html form
    def indoorNav(self, start=None, end=None):
        if start is None or end is None:
            return open("indoorNav.html")
        if start == "" and end == "":
            return open("indoorNav.html") 
        elif end == "":
            return "You can't travel nowhere?"
        elif start == "":
            return "You are not nowhere! Where are you starting your travels"
        else:
            try:
                shortPath = Dijkstra.Dijkstra("Nodes.sqlite3")

                doc = dominate.document(title='Dominate your HTML')

                with doc.head:
                    link(rel='stylesheet', type='text/css', href='static/css/indoorNav.css')

                with doc:
                    with div(id='header').add(ol()):
                        for i in shortPath.dijkstra(shortPath.return_graph(), start, end)[0]:
                            li(a(i.title()))

                    with div():
                        attr(cls='body')
                        p("The cost of this journey is {0}".format(shortPath.dijkstra(shortPath.return_graph(), start, end)[1]))

                return(str(doc))

            except TypeError as e:
                return e

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
        '/': {
            'tools.staticdir.root': current_dir,
            'tools.sessions.on': True,
            'tools.sessions.timeout': 15,
        },
        '/static': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': 'static',
        }
    }
cherrypy.quickstart(home(), '/', config)
