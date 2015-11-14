import pygame

from buffalo import utils

from chunk import Chunk
from mapManager import MapManager

class Camera:
    """
    Manages what is drawn on the screen
    and how it is drawn
    """

    zoom = 1.0
    pos  = 0, 0
    fPos = float(pos[0]), float(pos[1])
    locked = False
    marker = fPos # marker represents the last position at which chunks were loaded

    @staticmethod
    def lock(character, initial_update=False):
        """
        Lock the camera to a Character
        """
        Camera.locked = True
        Camera.character = character
        Camera.update(initial_update)
        

    @staticmethod
    def update(initial_update=False):
        if Camera.locked:
            x, y = Camera.character.fPos
            x, y = x - utils.SCREEN_W // 2, y - utils.SCREEN_H // 2
            Camera.updatePos((x, y))
        if initial_update:
            if Camera.locked:
                MapManager.hard_load(Camera.character.fPos)
            else:
                MapManager.hard_load(Camera.fPos)
            Camera.marker = Camera.fPos
            return
        if utils.dist(Camera.fPos, Camera.marker) > (Chunk.CHUNK_WIDTH * Chunk.TILE_SIZE):
            this_pos = Camera.character.fPos if Camera.locked else Camera.fPos
            MapManager.hard_load(this_pos)
            Camera.marker = Camera.fPos
        

    @staticmethod
    def updatePos(fPos):
        """
        The argument passed MUST be a tuple of two floating-point values
        """
        Camera.fPos = fPos
        Camera.pos = int(Camera.fPos[0]), int(Camera.fPos[1])
        # if fPos is somewhere where must load chunks
        # then load the chunks
        """
        THIS SHOULD REALLY BE A PROPERTY
        """

    @staticmethod
    def blitView():
        #Blits chunks
        rmult = Chunk.TILE_SIZE * Chunk.CHUNK_HEIGHT
        cmult = Chunk.TILE_SIZE * Chunk.CHUNK_WIDTH
        actualx = Camera.fPos[0] + utils.SCREEN_W / 2
        actualy = Camera.fPos[1] + utils.SCREEN_H / 2
        coords = MapManager.get_chunk_coords((actualx, actualy))
        for rowindx in range(coords[1] + MapManager.HARD_LOAD_TOP, coords[1] + MapManager.HARD_LOAD_BOTTOM + 1):
            for colindx in range(coords[0] + MapManager.HARD_LOAD_LEFT, coords[0] + MapManager.HARD_LOAD_RIGHT + 1):
                if not (colindx, rowindx) in MapManager.loaded_chunks.keys():
                    continue
                if not hasattr(MapManager.loaded_chunks[(colindx, rowindx)], 'surface'):
                    continue
                x = colindx
                y = rowindx
                chunk = MapManager.loaded_chunks[(colindx, rowindx)]
                chunk.blit(
                    utils.screen,
                    (cmult * x - Camera.pos[0], rmult * y - Camera.pos[1])
                )
        #Blits submaps
        for submap in MapManager.activeMap.submaps:
            submap.blit(utils.screen, (submap.pos[0] - Camera.pos[0], submap.pos[1] - Camera.pos[1]))
