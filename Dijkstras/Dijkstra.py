class Dijkstra():
    def __init__(self):
        self.__shortestPath = []
        self.__currentNode = 0
        self.__nodes = {"ECG-13": {"Connections": {"ECG-14": 5, "ECG-15": 7}, "Hidden": False},
                        "ECG-14": {"Connections": {"ECG-13": 3, "ECG-15": 5}, "Hidden": False},
                        "ECG-15": {"Connections": {"ECG-13": 2, "ECG-14": 5}, "Hidden": False},
                        "First Floor Stairs": {"Connections": {"ECG-13": 4, "ECG-14": 5, "ECG-15": 7}, "Hidden": False},
                        "Main Entrance": {"Connections": {"First Floor Stairs": 2}, "Hidden": False}
                        }

    def shortest_path(self, start, end):
        node_progress = {}

        for key in self.__nodes:
            node_progress[key] = {}

        while self.__currentNode != end:
            print("Dijkstra Here")
            break

        print(node_progress)

    def give_directions(self, start, end):
        pass

    def get_connections(self, name):
        for key in self.__nodes:
            if key == name:
                #print(len(self.__nodes[key]["Connections"]))
                return(self.__nodes[key]["Connections"])
        return []

if __name__ == "__main__":
    shortPath = Dijkstra()
    #print(shortPath.get_connections("Main Entrance"))
    shortPath.shortest_path("ECG-15", "ECG-14")
