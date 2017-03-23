import collections, math, pickle, sqlite3 as sql

class Graph:
	''' DataType to represent a graph. inspired by https://gist.github.com/econchick/4666413 
	
	Class Attributes:
	    self.verticies
	    Type: set
	    Stores the verticeis in the graph

	    self.edges
	    Type: dict
	    Stores the connecting edges for each vertex

	    self.weights
	    Type: dict
	    Stores a dictionary where the keys are touples. Each touple representing the distance
	    between the two verticies in the touple.

	'''

	def __init__(self):
		self.verticies = set()
		self.edges = collections.defaultdict(list)
		self.weights = {}

	def add_vertex(self, value):
		''' Add a new vertex to the graph '''
		self.verticies.add(value)

	def add_edge(self, from_vertex, to_vertex, distance):
		''' Adds a connection between two verticies by adding an entry to edges with
		the from and to node '''
		if from_vertex == to_vertex:
			pass
		self.edges[from_vertex].append(to_vertex)
		self.edges[to_vertex].append(from_vertex)
		self.weights[(from_vertex, to_vertex)] = distance
		self.weights[(to_vertex, from_vertex)] = distance
 
class Database:
	''' Database class which handles the storing and collection of data from "ECC_Building.sqlite3"
	
	Class Attributes
	self.connection
	Type: connection to 'ECC_Building.sqlite3'

	self.cursor
	Type: cursor
	Cursor to execute sql commands to database

	'''
	def __init__(self):
		self.connection = sql.connect('ECC_Building.sqlite3')
		self.cursor = self.connection.cursor()

	def add_vertex(self, vertex):
		''' Adds 'vertex' to the 'Verticies' table in the database '''

		self.cursor.execute(('INSERT INTO Verticies VALUES (?)'), (vertex,))
		self.connection.commit()

	def add_edge(self, edge):
		''' Adds 'edge' to the 'Edges' table in the database '''

		pdata = pickle.dumps(edge, pickle.HIGHEST_PROTOCOL)
		self.cursor.execute(('INSERT INTO Edges VALUES (?)'), (pdata,))
		self.connection.commit()

	def get_edges(self):
		''' Gets all the edges from the 'Edges' table in ECC_Building.sqlite3 and returns them in a list '''

		edges = []

		self.cursor.execute('SELECT * FROM Edges')

		while True:
			pdata = self.cursor.fetchone()
			if not pdata:
				break
			else:
				edge = pickle.loads(pdata[0])
				edges.append(edge)

		return edges

	def get_verticies(self):
		''' Gets all the verticies from the 'Verticies' table in ECC_Building.sqlite3 and returns them in a list '''

		verticies = []

		self.cursor.execute('SELECT * FROM Verticies')

		while True:
			vertex = self.cursor.fetchone()
			if not vertex:
				break
			else:
				verticies.append(vertex)

		return verticies


def dijkstra(graph, start_node):
	'''
	Method variables:
		visited
		Type: set
		Stores the values of visited nodes

		progress
		Type: dict
		Stores a node value with the distance to that node from the start node
		Key = Vertex in graph
		Value = distance to Vertex from start

		predecessors
		Type: dict
		Key = Node
		Value = Node which travled from to get to Key

	'''

	# init variables
	visited = set()

	# progress represents the distance from start -> vertex. It is created with each distance
	# being equal to 'math.inf' this is becuase we do not know the distance to any node yet.
	progress = dict.fromkeys(list(graph.verticies), math.inf)
	predecessors = dict.fromkeys(list(graph.verticies), None)

	# Update the start node in progress to the value 0.
	progress[start_node] = 0

	# While there is a node that is not in visited
	while visited != graph.verticies:
		# vertex becomes the closest node that has not yet been visited. It will begin at 'start_node'
		vertex = min((set(progress.keys()) - visited), key=progress.get)

		# for each node which is not in visited
		for neighborNode in set(graph.edges[vertex]) - visited:
			# New path is set to the current distance value in 'progress[vertex] 
			# plus the new weight distance'
			testPath = progress[vertex] + graph.weights[vertex, neighborNode]

			# If testPath is shorted than current path 'progress[neighborNode]'
			if testPath < progress[neighborNode]:
				# Update path to shorted 'testPath'
				progress[neighborNode] = testPath

				# Update previous vertex of the neighborNode
				predecessors[neighborNode] = vertex
		visited.add(vertex)
	return (progress, predecessors)

def short_path(graph, start, end):
	''' Uses the Dijkstra Method to return the shortest path from 'start' to 'end' '''

	# Update progress and predecessors with the dijkstra method
	progress, predecessors = dijkstra(graph, start)

	# init variables
	currentPath = []
	vertex = end

	while vertex != None:
		currentPath.append(vertex)
		vertex = predecessors[vertex]

	return(currentPath[::-1], progress[end])

if __name__ == '__main__':
	print("Running unit tests")

	# # Davids test graph // Uncomment to test
	# Graph = Graph()
	# # Verticies
	# Graph.add_vertex('a')
	# Graph.add_vertex('b')
	# Graph.add_vertex('c')
	# Graph.add_vertex('d')
	# Graph.add_vertex('e')
	# # Edges 
	# Graph.add_edge('a', 'b', 5)
	# Graph.add_edge('a', 'c', 6)
	# Graph.add_edge('a', 'd', 10)
	# Graph.add_edge('b', 'd', 6)
	# Graph.add_edge('c', 'd', 6)
	# Graph.add_edge('d', 'e', 2)

	# # ECC Building Graph // Stored in ECC_Building.sqlite3
	# Graph = Graph()
	# # #Verticies
	# Graph.add_vertex('ECG-13')
	# Graph.add_vertex('ECG-14')
	# Graph.add_vertex('ECG-15')
	# Graph.add_vertex('ECG-27')
	# Graph.add_vertex('Main Entrance')
	# Graph.add_vertex('First Floor Stairs')
	# # Edges
	# Graph.add_edge('ECG-13', 'ECG-14', 2)
	# Graph.add_edge('ECG-13', 'ECG-15', 4)
	# Graph.add_edge('ECG-14', 'ECG-15', 1)
	# Graph.add_edge('ECG-15', 'Main Entrance', 5)
	# Graph.add_edge('ECG-15', 'First Floor Stairs', 2)
	# Graph.add_edge('ECG-27', 'Main Entrance', 1)
	# Graph.add_edge('ECG-27', 'First Floor Stairs', 4)
	# Graph.add_edge('Main Entrance', 'First Floor Stairs', 3)

	# Unit Test for Dijkstra's Algorithm
	db = Database()
	Graph = Graph()

	edges = db.get_edges()
	verticies = db.get_verticies()

	for edge in edges:
		Graph.add_edge(edge[0][0], edge[0][1], edge[0][2])
	for vertex in verticies:
		Graph.add_vertex(vertex[0])

	for node in set(Graph.verticies):
		for vertex in set(Graph.verticies):
			print('From: {0}, To: {1}'.format(node, vertex), (short_path(Graph, node, vertex)))