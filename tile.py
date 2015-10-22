from serializable import Serializable
from buffalo import utils
from subMap import SubMap
from mapManager import MapManager

import os
import pygame

class Tile(Serializable):
    def __init__(self,pos=(0,0,0),type_id=0,collisionEnabled=False,buildingInternal=False,roofType=0,**kwargs):
        self.pos = pos
        self.type_id = type_id
        self.surface = utils.empty_surface((SubMap.TILE_SIZE,SubMap.TILE_SIZE))
        self.collisionEnabled = collisionEnabled
        self.buildingInternal=buildingInternal
        self.roofType=roofType
        self.inside=False
        self.IMG_FILE = ""
        self.renderedOnce = False
        self.render()

    def render(self):
        self.surface = utils.empty_surface((SubMap.TILE_SIZE,SubMap.TILE_SIZE))
        oldIMG_FILE = self.IMG_FILE
        if self.buildingInternal:
            if self.inside:
                self.IMG_FILE = os.path.join(os.path.join(*list(['tiles','assets'] + [str(self.type_id) + ".png"])))

            else:
                self.IMG_FILE = os.path.join(os.path.join(*list(['tiles','assets'] + [str(self.roofType) + ".png"])))

        else:
            self.IMG_FILE = os.path.join(os.path.join(*list(['tiles','assets'] + [str(self.type_id) + ".png"])))
        
        try:
            self.surface = pygame.image.load(self.IMG_FILE)
        except Exception as e:
            print("Error: Tile image for item \"" + str(self.type_id) + "\" does not exist.")
            print(e)
            self.IMG_FILE = os.path.join(os.path.join(*list(['tiles','assets'] + ["error.png"])))
            self.surface = pygame.image.load(self.IMG_FILE)
        self.renderedOnce = True

    def loadIDProperties(self):
        pass
