import sqlite3 as sql
import pickle


class Dijkstra:

	def __init__(self, db):
		self.conn = sql.connect(db)
		self.cur = self.conn.cursor()
		self.progress = []
		self.visited = set()
	
	def update_closet_nodes(self, node):
		if node in self.visited:
			print("In visited")
		else:
			connected = self.fetch_connections(node)
			for key in connected:
				if key in self.progress:
					print("In Progress")
				else:
					self.progress.append((node, key, connected[key]))
			self.visited.add(node)

	def loop(self, start, end):
		self.update_closet_nodes(start)
		print(self.progress)

	def fetch_connections(self, node):
		try:
			self.cur.execute(("Select * FROM Nodes WHERE Name = (?)"), (node,))
			currentNode = self.cur.fetchone()
			return(pickle.loads((currentNode[1])))
		except TypeError:
			print("That node does not exist!")

	def return_graph(self):
		graph = {}
		try:
			self.cur.execute("Select * FROM Nodes")
			while True:
				currentNode = self.cur.fetchone()
				if currentNode == None:
					break
				graph[currentNode[0]] = pickle.loads(currentNode[1])
			return graph
		except TypeError:
			print("There has been an error")


if __name__ == "__main__":
	shortPath = Dijkstra("Nodes.sqlite3")
	try:
		shortPath.loop("A", "B")
	finally:
		shortPath.conn.close()