import sqlite3 as sql
import pickle


class Dijkstra:
    def __init__(self):
        self.__usedNodes = []
        self.__currentNode = 0
        self.__nodes = {}

    def shortest_path(self, node):
        self.__currentNode = node
        self.__usedNodes = []

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

if __name__ == "__main__":
    shortPath = Dijkstra()
    try:
        shortPath.conn = sql.connect("Nodes.sqlite3")
        shortPath.cur = shortPath.conn.cursor()
        # shortPath.pickleStore("ECG-13", {"ECG-14": 5, "ECG-15": 3})
        # shortPath.pickleStore("ECG-14", {"ECG-13": 3, "ECG-15": 6})
        # shortPath.pickleStore("ECG-15", {"ECG-13": 3, "ECG-14": 6})
        # shortPath.pickleStore("ECG-27", {"Main Entrance": 1})
        # shortPath.pickleStore("First Floor Stairs", ["ECG-15"])
        print(shortPath.get_closest_node("ECG-15"))
    finally:
        shortPath.conn.close()

