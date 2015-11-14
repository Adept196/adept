import os
import copy
import time

from buffalo import utils

import mapManager

class SubMap:

    PATH = ["submaps"]
    TILE_SIZE = 32

    def __init__(self,_id,sizeX=0,sizeY=0,posX=0,posY=0,startingZ=0):
        self.size = sizeX,sizeY
        self.id = _id
        self.pos = posX,posY
        self.tileMap = list()
        self.fromFile()
        self.surface = utils.empty_surface((self.size[0] * SubMap.TILE_SIZE, self.size[1] * SubMap.TILE_SIZE))
        self.render(startingZ)        

    def toFile(self):
        LOAD_PATH = mapManager.MapManager.BASE_PATH + [mapManager.MapManager.activeMap.name] + SubMap.PATH
        url = os.path.join(*list(LOAD_PATH + [str(self.id) + '.smap']))

        output = ""
        for tile in self.tileMap:
            if tile is not None:
                    output += tile.serialize() + "\n"

        with open(url,'w+') as subMapFile:
            subMapFile.write(output)

    def fromFile(self):
        from tile import Tile
        LOAD_PATH = mapManager.MapManager.BASE_PATH + [mapManager.MapManager.activeMap.name] + SubMap.PATH
        url = os.path.join(*list(LOAD_PATH + [str(self.id) + '.smap']))
        if not os.path.isfile(url):
            print "Error: Tried to load SubMap with id \"" + str(self.id) + "\", but could not find the file."
            return
        maxX = 0
        maxY = 0
        with open(url,'r') as subMapFile:
            for tileLine in subMapFile:
                t = Tile.deserialize(tileLine)
                if t.pos[0] > maxX:
                    maxX = t.pos[0]
                if t.pos[1] > maxY:
                    maxY = t.pos[1]
                self.tileMap.append(t)
        self.size = maxX+1,maxY+1

    #Best practice to make sure there aren't duplicate tile objects at same point in tileMap
    def addTile(self, tile):
        self.removeTileAtLoc(tile.pos)
        self.tileMap.append(tile)

    def getTileAtPos(self,pos):
        for tile in self.tileMap:
            if tile.pos[0] == pos[0] and tile.pos[1] == pos[1] and tile.pos[2] == pos[2]:
                return tile

    def removeTileAtLoc(self,pos):
        for tile in self.tileMap:
            if tile.pos[0] == pos[0] and tile.pos[1] == pos[1] and tile.pos[2] == pos[2]:
                self.tileMap.remove(tile)

    def render(self,zLevel):
        newSurface = utils.empty_surface((self.size[0] * SubMap.TILE_SIZE, self.size[1] * SubMap.TILE_SIZE))
        for tile in self.tileMap:
            if tile is not None:
                if tile.pos[2] == zLevel:
                        tile.render()
                        newSurface.blit(tile.surface, (SubMap.TILE_SIZE * tile.pos[0], SubMap.TILE_SIZE * tile.pos[1]))
        self.surface = newSurface
        self.surface = newSurface
                

    def blit(self, dest, pos):
        dest.blit( self.surface, pos )

    def handleCollision(self, tile, pc):
        tilesChanged = False
        if tile is not None and tile.buildingInternal:
            tiles = copy.deepcopy(self.tileMap)
            for tile in tiles:
                if tile.buildingInternal and not tile.inside:
                    self.getTileAtPos(tile.pos).inside = True
                    tilesChanged = True
        else:
            for tile in self.tileMap:
                if tile.buildingInternal and tile.inside:
                    tile.inside = False
                    tilesChanged = True
        if tilesChanged:
            self.render(pc.zLevel)

    def getTileAtCoord(self, pos):
        x = (pos[0] - self.pos[0]) / SubMap.TILE_SIZE
        y = (pos[1] - self.pos[1]) / SubMap.TILE_SIZE
        return self.getTileAtPos((int(x),int(y),0))

    # def findAllNeighbors(self,tile):
    #     neighbors_found = 1
    #     neighbors = [tile]
    #     while neighbors_found is not 0:
    #         neighbors_found = 0
    #         for t in neighbors:
    #             immediateNeighbors = list()
    #             immediateNeighbors.append(self.getTileAtPos((t.pos[0]+1,t.pos[1],t.pos[2])))
    #             immediateNeighbors.append(self.getTileAtPos((t.pos[0]-1,t.pos[1],t.pos[2])))
    #             immediateNeighbors.append(self.getTileAtPos((t.pos[0],t.pos[1]+1,t.pos[2])))
    #             immediateNeighbors.append(self.getTileAtPos((t.pos[0],t.pos[1]-1,t.pos[2])))
    #             immediateNeighbors.append(self.getTileAtPos((t.pos[0],t.pos[1]-1,t.pos[2])))
    #             immediateNeighbors.append(self.getTileAtPos((t.pos[0],t.pos[1]-1,t.pos[2])))
    #             immediateNeighbors.append(self.getTileAtPos((t.pos[0],t.pos[1]-1,t.pos[2])))
    #             for n in immediateNeighbors:
    #                 if n is not None and n.buildingInternal is True and not n in neighbors:
    #                     neighbors.append(n)
    #                     neighbors_found += 1
    #     return neighbors
