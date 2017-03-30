import cherrypy
import os
import os.path
import security
import Pathfinding
import dominate
from dominate.tags import *


class home():
    @cherrypy.expose
    def index(self):
        return open("campusMap.html")

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
            return open("logoff.html")
        if username is None or userpassword is None:
            return open("admin.html")
        with security.Security() as password_check:
            try:
                password_check.log_on(username, userpassword)
                # replace with successful page
                cherrypy.session["loggedon"] = True
                return open("logoff.html")
            except ValueError:
                # replace with unsuccessful page
                return open("adminFailLogin.html")

    @cherrypy.expose
    def ecBuildingNav(self, start=None, end=None):
        if start is None or end is None:
            return open("ecBuildingNav.html")
        elif start is "" or end is "":
            return open("ecBuildingNav.html")
        else:
            try:
                edges = Pathfinding.Database.get_edges(Pathfinding.Database())
                vertices = Pathfinding.Database.get_vertices(Pathfinding.Database())
                graph = Pathfinding.Graph() # Create graph object
                # Populate graph with nodes from the database
                for edge in edges:
                    graph.add_edge(edge[0], edge[1], edge[2])
                for vertex in vertices:
                    graph.add_vertex(vertex)

                path, distance = Pathfinding.short_path(graph, start, end) # Use dijstras alg to find the shorted path and distance

                # Use dominate to create a HTML page with a list populated with the path and distance
                doc = dominate.document(title='Indoor Navigation')
                with doc.head:
                    link(rel='stylesheet', type='text/css',
                         href='static/css/ecBuildingNav.css')

                with doc:
                    with div(id='header').add(ol()):
                        for i in path:
                            li(a(i.title()))

                    with div():
                        attr(cls='body')
                        p("The cost of this journey is {0}".format(distance))

                # Return the HTML page. Cherrpy then displays this page
                return str(doc)

            except TypeError as e:
                print("Your starting point or destination is not in the graph")
                print(e)

    def logoff(self):
        cherrypy.session["loggedon"] = False
        return self.index()


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
