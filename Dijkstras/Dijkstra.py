import sqlite3 as sql
import pickle

class Dijkstra():
    def __init__(self):
        self.__shortestPath = []
        self.__currentNode = 0
        self.__nodes = {}

    def shortestPath(self):
        pass

    def pickleStore(self, node, connections):
        cur = self.conn.cursor()
        pdata = pickle.dumps(connections, pickle.HIGHEST_PROTOCOL)
        cur.execute(("INSERT INTO Nodes VALUES (?, ?)"), (node, pdata))
        self.conn.commit()

    def unPickleFetch(self, node):
        try:
            nodeInfo = []
            cur = self.conn.cursor()
            cur.execute(("Select * FROM Nodes WHERE Name = (?)"), (node,))
            currentNode = cur.fetchone()
            nodeInfo.append(currentNode[0])
            nodeInfo.append(pickle.loads(currentNode[1]))
            print(nodeInfo)
        except TypeError:
            print("That node does not exist!")

    def fetchConnections(self, node):
        try:
            cur = self.conn.cursor()
            cur.execute(("Select * FROM Nodes WHERE Name = (?)"), (node,))
            currentNode = cur.fetchone()
            print(pickle.loads((currentNode[1])))
        except TypeError:
            print("That node does not exist!")

    def getClosestNode(self, node):
        try:
            cur = self.conn.cursor()
            cur.execute(("Select * FROM Nodes WHERE Name = (?)"), (node,))
            currentNode = cur.fetchone()
            currentNode = pickle.loads(currentNode[1])
            print(min(currentNode, key=currentNode.get))
        except TypeError:
            print("That node does not exist!")

if __name__ == "__main__":
    shortPath = Dijkstra()
    try:
        shortPath.conn = sql.connect("Nodes.sqlite3")
        # shortPath.pickleStore("ECG-13", {"ECG-14": 5, "ECG-15": 3})
        # shortPath.pickleStore("ECG-14", {"ECG-13": 3, "ECG-15": 6})
        # shortPath.pickleStore("ECG-15", {"ECG-13": 3, "ECG-14": 6})
        # shortPath.pickleStore("ECG-27", {"Main Entrance": 1})
        # shortPath.pickleStore("First Floor Stairs", ["ECG-15"])
        # shortPath.unPickleFetch("ECG-15")
    finally:
        shortPath.conn.close()

