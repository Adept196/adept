import os
#from multiprocessing import Process, Queue
from threading import Thread
from Queue import Queue

from buffalo import utils

import Map
import pluginManager
import chunk

class MapManager:
    """
    Manages chunks and map loading
    """

    BASE_PATH    = ["maps"] # BASE_PATH is a list version of the base path in
                            # which MapManager will search for chunks. For example,
                            # if the base path should be maps/otherfolder/ then
                            # BASE_PATH should equal ["maps", "otherfolder"]
    maps          = []      # Maps is a list of all Map's found in within BASE_PATH
    activeMap     = None    # activeMap is the active map // lol

    loaded_chunks = dict()
    lru_chunks    = dict()  # least recently used chunks

    HARD_LOAD_LEFT   = -5
    HARD_LOAD_RIGHT  =  5
    HARD_LOAD_TOP    = -5
    HARD_LOAD_BOTTOM =  5

    @staticmethod
    def loadMaps():
        """
        loadMaps loads all the maps that are checked in the plugins manager file
        """
        for name in pluginManager.PluginManager.mapNames:
            MapManager.loadMap(name)
        MapManager.maps.sort(key=lambda m: m.precedence)
        MapManager.activeMap = MapManager.maps[0]
        # THIS LINE IS REALLY IMPORTANT
        MapManager.soft_load_reader_queue = Queue()
        MapManager.soft_load_writer_queue = Queue()

    @staticmethod
    def loadMap(map_name):
        """
        loadMap takes one string map_name and attempts to load the corresponding map
        """
        CHUNK_PATH_LIST = MapManager.BASE_PATH + [map_name, "chunks"]
        MapManager.maps.append(Map.Map(map_name, CHUNK_PATH_LIST))

    @staticmethod
    def get_chunk_coords(world_pos):
        return (
            int(world_pos[0] / (chunk.Chunk.CHUNK_WIDTH * chunk.Chunk.TILE_SIZE)),
            int(world_pos[1] / (chunk.Chunk.CHUNK_HEIGHT * chunk.Chunk.TILE_SIZE)),
        )

    @staticmethod
    def hard_load(world_pos):
        x, y = MapManager.get_chunk_coords(world_pos)
        for j in range(y + MapManager.HARD_LOAD_TOP, y + MapManager.HARD_LOAD_BOTTOM + 1):
            for i in range(x + MapManager.HARD_LOAD_LEFT, x + MapManager.HARD_LOAD_RIGHT + 1):
                if (i, j) not in MapManager.loaded_chunks.keys():
                    MapManager.loaded_chunks[(i, j)] = chunk.Chunk(i, j)
                    MapManager.lru_chunks[(i, j)] = 2
        if hasattr(MapManager, 'soft_load_reader_thread'):
            MapManager.soft_load_reader_thread.join()
        MapManager.soft_load_reader_thread = MapManager.get_soft_load_reader_thread()
        MapManager.soft_load_reader_thread.start()
        MapManager.soft_load_reader_queue.put(world_pos)
        MapManager.soft_load_reader_queue.put("DONE")

    @staticmethod
    def soft_load(world_pos):
        x, y = MapManager.get_chunk_coords(world_pos)
        for j in range(y + MapManager.HARD_LOAD_TOP, y + MapManager.HARD_LOAD_BOTTOM + 1): # sides
            for i in range(x + MapManager.HARD_LOAD_LEFT - 1, x + MapManager.HARD_LOAD_LEFT) + range(x + MapManager.HARD_LOAD_RIGHT + 1, x + MapManager.HARD_LOAD_RIGHT + 2):
                #MapManager.loaded_chunks[(i, j)] = chunk.Chunk(i, j)
                if (i, j) not in MapManager.loaded_chunks:
                    package = ((x, y), (i, j), chunk.Chunk(i, j, from_other_thread=False), 0) # zero means create surface,  means render
                    MapManager.soft_load_writer_queue.put(package)
        for j in range(y + MapManager.HARD_LOAD_TOP - 1, y + MapManager.HARD_LOAD_TOP) + range(y + MapManager.HARD_LOAD_BOTTOM + 1, y + MapManager.HARD_LOAD_BOTTOM + 2): # top and bottom
            for i in range(x + MapManager.HARD_LOAD_LEFT - 1, x + MapManager.HARD_LOAD_RIGHT + 2): 
                #MapManager.loaded_chunks[(i, j)] = chunk.Chunk(i, j)
                if (i, j) not in MapManager.loaded_chunks:
                    package = ((x, y), (i, j), chunk.Chunk(i, j, from_other_thread=False), 0) # zero means create surface,  means render
                    MapManager.soft_load_writer_queue.put(package)

    @staticmethod
    def offload_old_chunks():
        # This method goes through the lru_chunks dictionary
        # and determines which chunks don't need to be in memory
        # based on when they were last used relative to other chunks
        for key in MapManager.lru_chunks.keys():
            if MapManager.lru_chunks[key] == 0:
                if key in MapManager.loaded_chunks.keys():
                    del MapManager.loaded_chunks[key]
                del MapManger.lru_chunks[key]

    @staticmethod
    def soft_load_reader():
        while True:
            world_pos = MapManager.soft_load_reader_queue.get()
            if world_pos == "DONE":
                break
            else:
                MapManager.soft_load(world_pos)

    @staticmethod
    def soft_load_writer():
        if MapManager.soft_load_writer_queue.empty():
            return
        package = MapManager.soft_load_writer_queue.get()
        coords, pos, chunk, action = package
        if action is 0:
            chunk.create_surface()
            MapManager.loaded_chunks[pos] = chunk

            ##### LRU STUFF
            if pos in MapManager.lru_chunks.keys():
                MapManager.lru_chunks[pos] = 1
            else:
                MapManager.lru_chunks[pos] = 1
            x, y = coords
            for i, j in MapManager.loaded_chunks.keys():
                if i < x + MapManager.HARD_LOAD_LEFT or i > x + MapManager.HARD_LOAD_RIGHT or j < y + MapManager.HARD_LOAD_TOP or j > y + MapManager.HARD_LOAD_BOTTOM:
                    # these  are really far away chunks that can be offloaded if necessary
                    MapManager.lru_chunks[i, j] = 0
            #### LRU STUFF

            new_package = (None, pos, None, 1)
            MapManager.soft_load_writer_queue.put(new_package)

        elif action is 1:
            MapManager.loaded_chunks[pos].render()

    @staticmethod
    def get_soft_load_reader_thread():
        soft_load_reader_thread = Thread(target=MapManager.soft_load_reader)
        soft_load_reader_thread.daemon = True
        return soft_load_reader_thread
