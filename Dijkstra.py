import sqlite3 as sql # Import the sqlite3 modeule to access and store Nodes/Graph
import pickle # Import pickle to unpickle Dictinarys from sqlite3 database


class Dijkstra:

    def __init__(self, db):
        # Connect to the sqlite3 database which contains all the nodes
        self.conn = sql.connect(db)
        # Create cursor and connect it to the sqlite3 database
        self.cur = self.conn.cursor()

    def dijkstra(self, graph, start, end, visited = [], distances = {}, predecessors = {}):
        ''' Implimentation of Dijkstras algorithm. Arguments are the graph of the nodes. The Node at which the navigation will start at
            The end node which is the destination of the route. '''
        if start not in graph or end not in graph:
            # If the start node or end node isn't in the graph then stop the
            # function.
            raise TypeError("The start or end node is not in your graph")

        if start == end:  # Base case for the recursive call
            path = []
            pred = end
            # Populate pred list which route taken using predecessors (dict)
            while pred != None:
                path.append(pred)
                pred = predecessors.get(pred, None)
            # self.give_directions(path[::-1], str(distances[end]))
            return (path[::-1], str(distances[end]))
        else:
            if not visited:
                distances[start] = 0
            for neighbor in graph[start]:
                if neighbor not in visited:
                    new_distance = distances[start] + graph[start][neighbor]
                    if new_distance < distances.get(neighbor, float("inf")):
                        distances[neighbor] = new_distance
                        predecessors[neighbor] = start
            visited.append(start) # Add start to visited list so that it is not reused
            unvisited = {}
            for node in graph:
                if node not in visited:
                    unvisited[node] = distances.get(node, float("inf"))
            nextNode = min(unvisited, key=unvisited.get)
            return self.dijkstra(graph, nextNode, end, visited, distances, predecessors) # Recursive call

    def return_graph(self):
        ''' Returns the graph needed for the dijkstra function. This function collects the graph from the sqlite3 database '''
        graph = {}
        try:
            # Select everything from the "Nodes" table
            self.cur.execute("Select * FROM Nodes")
            while True:
                # Get the next row from the Nodes table
                currentNode = self.cur.fetchone()
                # If the fetched row is of "NoneType" exit out of the loop
                if currentNode == None:
                    break
                # Unpickle the row to return a "Dict" for each node in the
                # graph
                graph[currentNode[0]] = pickle.loads(currentNode[1])
        except TypeError:
            print("There has been an error")
        return graph

    def pickle_store(self, node, connections):
        ''' Pickle and store a node and its connections in the sqlite3 database
            "Format // "name of node, {connection name: connection distance}" '''
        pdata = pickle.dumps(
            connections, pickle.HIGHEST_PROTOCOL)  # Pickle the graph entry (Node, Connections)
        # insert the name of the node and the pickled data into the sqlite3
        # database
        self.cur.execute(("INSERT INTO Nodes VALUES (?, ?)"), (node, pdata))
        self.conn.commit()

    def pickle_fetch(self, node):
        ''' Unpickles and returns the dictionary stored in the "Nodes" table which is equal to "node" '''
        try:
            nodeInfo = []
            # Fetch all data which is in the "Nodes" table which is equal to
            # the "node" value.
            self.cur.execute(("Select * FROM Nodes WHERE Name = (?)"), (node,))
            # No need for a loop as there should only be one value returned.
            currentNode = self.cur.fetchone()
            nodeInfo.append(currentNode[0])
            nodeInfo.append(pickle.loads(currentNode[1]))
            return(nodeInfo)
        except TypeError:
            # If "node" is not in the sqlite3 database then notify the user.
            print("That node does not exist!")

    def give_directions(self, path, cost):
        path = (list(enumerate(path, start = 1)))

        for node in path:
            print("{0}: Go to {1}".format(node[0], node[1]))

        print("The cost of this journey is: " + cost)

if __name__ == "__main__":
    shortPath = Dijkstra("Nodes.sqlite3")

    # Test graph
    # shortPath.dijkstra(shortPath.return_graph(), "A", "E")
    # shortPath.pickle_store("A", {"B": 5, "C": 6, "D": 10})
    # shortPath.pickle_store("B", {"A": 5, "D": 6})
    # shortPath.pickle_store("C", {"A": 6, "D": 6})
    # shortPath.pickle_store("D", {"A": 10, "B": 6, "C": 6, "E": 2})
    # shortPath.pickle_store("E", {"D": 2})

    print(shortPath.dijkstra(shortPath.return_graph(), "Main Entrance", "ECG-15"))
    # shortPath.pickle_store("ECG-13", {"ECG-14": 5, "ECG-15": 5})
    # shortPath.pickle_store("ECG-14", {"ECG-15": 6, "ECG-13": 5})
    # shortPath.pickle_store("ECG-15", {"ECG-13": 5, "ECG-14": 6})
    # shortPath.pickle_store("First Floor Stairs", {"ECG-15": 8, "ECG-27": 3, "Main Entrance": 2})
    # shortPath.pickle_store("Main Entrance", {"ECG-27": 2, "First Floor Stairs": 2})
    # shortPath.pickle_store("", {})