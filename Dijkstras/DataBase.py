import pickle

doc = open("Database and Algs/nodes.txt", "wb")
#
rooms = {"ECG-13": {"Connections": {"ECG-14": 5, "ECG-15": 7}, "Hidden": False},\
         "ECG-14": {"Connections": {"ECG-13": 3, "ECG-15": 5}, "Hidden": False},\
         "ECG-15": {"Connections": {"ECG-13": 2, "ECG-14": 5}, "Hidden": False},\
         "First Floor Stairs": {"Connections": {"ECG-13": 4, "ECG-14": 5, "ECG-15": 7}, "Hidden": False},\
         "Main Entrance": {"Connections": {"First Floor Stairs": 2}, "Hidden": False}
        }

pickle.dump(rooms, doc)

# room = pickle.load(doc)
# print(room[0])
