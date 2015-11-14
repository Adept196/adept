import os

import pygame

from buffalo import utils

import serializable
import subMap

class Tile(serializable.Serializable, object):

    TILE_SIZE = 32

    LOADED_SURFACES = dict()

    DEFAULT_USE_IMAGES = True
    DEFAULT_BASE_COLOR = (100, 180, 0, 255)
    DEFAULT_MEAN_TEMP  = 70 # degrees Fahrenheit
    DEFAULT_VAR_TEMP   = 10 # degrees Fahrenheit
    DEFAULT_MEAN_HUM   = 0.3 # percent / 100
    DEFAULT_VAR_HUM    = 0.1 # percent / 100
    DEFAULT_MEAN_NC    = 100 # grams
    DEFAULT_VAR_NC     = 50 # grams

    def __init__(
            self,
            pos=(0, 0, 0),
            type_id=0,
            collisionEnabled=False,
            buildingInternal=False,
            roofType=0,
            heightLevel=0,
            **kwargs
    ):
        self.pos = pos
        self.type_id = type_id
        self.surface = utils.empty_surface((subMap.SubMap.TILE_SIZE, subMap.SubMap.TILE_SIZE))
        self.collisionEnabled = collisionEnabled
        self.buildingInternal = buildingInternal
        self.roofType = roofType
        self.inside = False
        self.heightLevel = heightLevel
        self.use_images = kwargs.get('use_images') if kwargs.get('use_images') is not None else Tile.DEFAULT_USE_IMAGES
        self.base_color = kwargs.get('base_color') if kwargs.get('base_color') is not None else Tile.DEFAULT_BASE_COLOR
        self.mean_temp = kwargs.get('mean_temp') if kwargs.get('mean_temp') is not None else Tile.DEFAULT_MEAN_TEMP
        self.var_temp = kwargs.get('var_temp') if kwargs.get('var_temp') is not None else Tile.DEFAULT_VAR_TEMP
        self.mean_hum = kwargs.get('mean_hum') if kwargs.get('mean_hum') is not None else Tile.DEFAULT_MEAN_HUM
        self.var_hum = kwargs.get('var_hum') if kwargs.get('var_hum') is not None else Tile.DEFAULT_VAR_HUM
        self.mean_nc = kwargs.get('mean_nc') if kwargs.get('mean_nc') is not None else Tile.DEFAULT_MEAN_NC
        self.var_nc = kwargs.get('var_nc') if kwargs.get('var_nc') is not None else Tile.DEFAULT_VAR_NC
        self.render()

    def render(self):
        if self.use_images:
            renderID = self.type_id
            if self.buildingInternal and not self.inside:
                renderID = self.roofType
            self.surface = Tile.loadSurfaceForId(renderID)
        else:
            #self.surface = utils.empty_surface((32, 32))
            #self.surface.fill(self.base_color)
            pass

    def blit(self, dest, pos=(0,0)):
        if self.use_images:
            renderID = self.type_id
            if self.buildingInternal and not self.inside:
                renderID = self.roofType
            dest.blit(Tile.loadSurfaceForId(renderID), self.pos[:2])
        else:
            dest.fill(
                self.base_color,
                pygame.Rect(
                    (self.pos[0] + pos[0], self.pos[1] + pos[1]),
                    (Tile.TILE_SIZE, Tile.TILE_SIZE),
                )
            )

    def onCollision(self, pc=None):
        pass

    @staticmethod
    def loadSurfaceForId(_id):
        if _id in Tile.LOADED_SURFACES.keys():
            return Tile.LOADED_SURFACES[_id]
        IMG_FILE = os.path.join(os.path.join(*list(['assets','terrain'] + [str(_id) + ".png"])))
        try:
            Tile.LOADED_SURFACES[_id] = pygame.image.load(IMG_FILE)
            return Tile.LOADED_SURFACES[_id]
        except Exception as e:
            print("Error: Chunk texture for item \"" + str(_id) + "\" does not exist.")
            print(e)
            IMG_FILE = os.path.join(os.path.join(*list(['assets'] + ["error.png"])))
            Tile.LOADED_SURFACES[_id] = pygame.image.load(IMG_FILE)
            return Tile.LOADED_SURFACES[_id]
