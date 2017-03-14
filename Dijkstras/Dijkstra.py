import sqlite3 as sql
import pickle


class Dijkstra:

    def __init__(self, db):
        self.conn = sql.connect(db)
        self.cur = self.conn.cursor()

    def dijkstra(self, graph, start, end, visited=[], distances={}, predecessors={}):
        if start not in graph or end not in graph:
            raise TypeError("The start or end node is not in your graph")

        if start == end:
            path = []
            pred = end
            while pred != None:
                path.append(pred)
                pred = predecessors.get(pred, None)
            print(
                "shortest path: "+str((path[::-1]))+" cost="+str(distances[end]))
        else:
            if not visited:
                distances[start] = 0
            for neighbor in graph[start]:
                if neighbor not in visited:
                    new_distance = distances[start] + graph[start][neighbor]
                    if new_distance < distances.get(neighbor, float("inf")):
                        distances[neighbor] = new_distance
                        predecessors[neighbor] = start
            visited.append(start)
            unvisited = {}
            for node in graph:
                if node not in visited:
                    unvisited[node] = distances.get(node, float("inf"))
            nextNode = min(unvisited, key=unvisited.get)
            self.dijkstra(graph, nextNode, end, visited, distances, predecessors)

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
        return graph

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


if __name__ == "__main__":
    shortPath = Dijkstra("Nodes.sqlite3")
    shortPath.dijkstra(shortPath.return_graph(), "Main Entrance", "ECG-15")
    # shortPath.dijkstra(shortPath.return_graph(), "A", "E")

    # Test graph 
    # shortPath.pickle_store("A", {"B": 5, "C": 6, "D": 10})
    # shortPath.pickle_store("B", {"A": 5, "D": 6})
    # shortPath.pickle_store("C", {"A": 6, "D": 6})
    # shortPath.pickle_store("D", {"A": 10, "B": 6, "C": 6, "E": 2})
    # shortPath.pickle_store("E", {"D": 2})

    # shortPath.pickle_store("ECG-13", {"ECG-14": 5, "ECG-15": 5})
    # shortPath.pickle_store("ECG-14", {"ECG-15": 6, "ECG-13": 5})
    # shortPath.pickle_store("ECG-15", {"ECG-13": 5, "ECG-14": 6})
    # shortPath.pickle_store("First Floor Stairs", {"ECG-15": 8, "ECG-27": 3, "Main Entrance": 2})
    # shortPath.pickle_store("Main Entrance", {"ECG-27": 2, "First Floor Stairs": 2})
