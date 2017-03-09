import sqlite3 as sql
import pickle


class Dijkstra:

    def __init__(self, db):
        self.conn = sql.connect(db)
        self.cur = self.conn.cursor()
        self.__graph = {}
        self.__visited = []

    def start(self, graph, start, end):
        # progress = {node: [previously visited nodes], distance}
        self.__graph[start] = [["ECG-15"], 0]
        #del graph[start]
        for key in graph:
            if key != start:
                self.__graph[key] = [[], float("inf")]

        currentNode = start
        self.short_path(currentNode, end)

    def short_path(self, currentNode, end):
        if currentNode == end:
            print("Done")
            print(self.__graph[currentNode])
        elif currentNode in self.__visited:
            notUsed = {}
            print("Already Used This Node")
            connections = self.fetch_connections(currentNode)
            print(connections, self.__visited, currentNode)
            for key in connections:
                if len(connections) != 0:
                    if key not in self.__visited:
                        notUsed[key] = connections[key]

            if len(notUsed) != 0:
                currentNode = self.get_closest(notUsed)
                currentNode = currentNode[0]
                self.__visited.append(currentNode)
                self.short_path(currentNode, end)
            else:
                print("There is no route")

        else:
            self.__visited.append(currentNode)
            connections = self.fetch_connections(currentNode)
            print(connections, self.__visited)

            for key in connections:
                self.__graph[key][0].append(currentNode)
                if self.__graph[key][1] == float("inf"):
                    self.__graph[key][1] = 0
                self.__graph[key][1] = (self.__graph[key][1] + connections[key])

            for index in self.__visited:
                try:
                    del connections[index]
                except KeyError:
                    pass

            currentNode = self.get_closest(connections)
            currentNode = currentNode[0]
            self.__visited.append(currentNode)
            self.short_path(currentNode, end)

    def get_closest(self, connections):
        closest = []
        closest.append((min(connections, key=connections.get)))
        closest.append(connections[closest[0]])
        return(closest)

    def pickle_store(self, node, connections):
        cur = self.conn.cursor()
        pdata = pickle.dumps(connections, pickle.HIGHEST_PROTOCOL)
        cur.execute(("INSERT INTO Nodes VALUES (?, ?)"), (node, pdata))
        self.conn.commit()

    def pickle_fetch(self, node):
        try:
            nodeInfo = []
            self.cur.execute(("Select * FROM Nodes WHERE Name = (?)"), (node,))
            currentNode = self.cur.fetchone()
            nodeInfo.append(currentNode[0])
            nodeInfo.append(pickle.loads(currentNode[1]))
            return(nodeInfo)
        except TypeError:
            print("That node does not exist!")

    def fetch_connections(self, node):
        try:
            self.cur.execute(("Select * FROM Nodes WHERE Name = (?)"), (node,))
            currentNode = self.cur.fetchone()
            return(pickle.loads((currentNode[1])))
        except TypeError:
            print("That node does not exist!")

    def get_closest_node(self, node):
        try:
            closest = []
            self.cur.execute(("Select * FROM Nodes WHERE Name = (?)"), (node,))
            currentNode = self.cur.fetchone()
            currentNode = pickle.loads(currentNode[1])
            closest.append((min(currentNode, key=currentNode.get)))
            closest.append(currentNode[closest[0]])
            return closest
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
        # shortPath.pickle_store("ECG-13", {"ECG-14": 5, "ECG-15": 3})
        # shortPath.pickle_store("ECG-14", {"ECG-13": 3, "ECG-15": 6})
        # shortPath.pickle_store("ECG-15", {"ECG-13": 3, "ECG-14": 6, "First Floor Stairs": 4})
        # shortPath.pickle_store("ECG-27", {"Main Entrance": 1})
        # shortPath.pickle_store("First Floor Stairs", {"ECG-15": 4})
        # shortPath.pickle_store("Main Entrance", {"ECG-27": 1})
        shortPath.start(shortPath.return_graph(), "ECG-15", "First Floor Stairs")
    finally:
        shortPath.conn.close()
