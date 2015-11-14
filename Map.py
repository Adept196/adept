import os, re

import mapManager

class Map:
    def __init__(self, name, BASE_PATH_LIST):
        self.name = name
        self.BASE_PATH_LIST = BASE_PATH_LIST
        self.pathlist = mapManager.MapManager.BASE_PATH + [self.name,]
        self.path = os.path.join(*self.pathlist)
        self.precedence = 0
        self.seed = 0
        self.submaps = list()
        path = os.path.join(*list(self.pathlist + ["properties.txt"]))
        if not os.path.isfile(path):
            print ("[Map] Error: No properties.txt found at \"" + path + "\". Creating an empty one.")
            if not os.path.exists(os.path.dirname(path)):
                os.makedirs(os.path.dirname(path))
            with open(path, 'w+') as pfile:
                pass
        with open(os.path.join(*list(mapManager.MapManager.BASE_PATH + [self.name, "properties.txt"]))) as mfile:
            for line in mfile:
                words = line.split()
                if len(words) >= 2:
                    if words[0] == "precedence":
                        try:
                            self.precedence = int(words[1])
                        except:  # If the second word can't be converted to an int
                            pass # Then don't do anything; keep precedence of 0
                    if words[0] == "seed":
                        try:
                            self.seed = float(words[1])
                        except:
                            pass
        self.loadChunkFiles()
        self.loadSubMaps()

    def loadChunkFiles(self):
        LOAD_PATH = self.pathlist + ["chunks"]
        if not os.path.exists(os.path.join(*LOAD_PATH)):
            print("[Map] Error: No chunks folder found. Creating an empty one.")
            os.makedirs(os.path.join(*LOAD_PATH))
        files = [f for f in os.listdir(os.path.join(*LOAD_PATH)) if os.path.isfile(os.path.join(*list(LOAD_PATH + [f])))]
        self.chunk_files = [os.path.join(*list(LOAD_PATH + [f])) for f in files if len(f) >= 9 and f[-6:] == ".chunk"]

    def loadSubMaps(self):
        LOAD_PATH = self.pathlist + ["submaps"]
        if not os.path.exists(os.path.join(*LOAD_PATH)):
            print("[Map] Error: No submaps folder found. Creating an empty one.")
            os.makedirs(os.path.join(*LOAD_PATH))
        files = [f for f in os.listdir(os.path.join(*LOAD_PATH)) if os.path.isfile(os.path.join(*list(LOAD_PATH + [f])))]
        self.chunk_files = [os.path.join(*list(LOAD_PATH + [f])) for f in files if f.endswith(".smap")]


