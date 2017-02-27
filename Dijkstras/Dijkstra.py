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

    def unpickleFetch(self, node):
        try:
            cur = self.conn.cursor()
            cur.execute(("Select * FROM Nodes WHERE Name = (?)"), (node,))
            currentNode = cur.fetchone()
            print(pickle.loads((currentNode[1])))
        except TypeError:
            print("That node does not exist!")


if __name__ == "__main__":
    shortPath = Dijkstra()
    try:
        shortPath.conn = sql.connect("Nodes.sqlite3")
        #shortPath.pickleStore("ECG-15", [1,2,3])
        #shortPath.unpickleFetch("ECG-15")
    finally:
        shortPath.conn.close()

