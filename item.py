from enum import Enum
from buffalo import utils
import yaml
import os
import random
import pygame
from inventoryUI import InventoryUI

class Item():
    BASE_PATH = ["items"]

    def __init__(self,name,quantity=0,durability=1.0):
        """
        Static item information
        """
        self.name = name
        self.info = dict()

        ITEM_FILE = os.path.join(os.path.join(*list(Item.BASE_PATH + [self.name + ".yml"])))
        try:
            with open(ITEM_FILE, "r") as iFile:
                self.info = yaml.load(iFile.read())
        except Exception as e:
            print "Error: Item \"" + name + "\" does not exist."


        """
        Special Values per Type:
        ------------------------
            - Weapon:
                -Base Damage
                -Base Attack Speed
                -Durability per Use
                -Critical Chance
                -Critical Multiplier
            - Tool:
                -Base Damage
                -Base Attack Speed
                -Durability per Use
            - Quest:
                -Quest ID
            - Armor:
                -Body Part
                -Base Protection
            - Resource:
                -Resource Type
        ------------------------
        """

        """
        Instance variables
        """
        self.quantity = quantity
        self.durability = durability
        self.instanceID = random.random()
        self.surface = utils.empty_surface((InventoryUI.BUTTON_SIZE, InventoryUI.BUTTON_SIZE))
        #Load item image to surface
        IMG_FILE = os.path.join(os.path.join(*list(Item.BASE_PATH +  ['assets'] + [self.name + ".png"])))
        try:
            self.surface = pygame.image.load(IMG_FILE)
        except Exception as e:
            print "Error: Icon for item \"" + str(name) + "\" does not exist."
            print e
            IMG_FILE = os.path.join(os.path.join(*list(Item.BASE_PATH +  ['assets'] + ["error.png"])))
            self.surface = pygame.image.load(IMG_FILE)
        self.renderItemQuantity()

    def renderItemQuantity(self):
        if(self.quantity > 1):
            myfont = pygame.font.SysFont("monospace", 15)
            label = myfont.render(str(self.quantity), 1, (255,255,0))
            self.surface.blit(label, (12,18))

    def update(self):
        self.renderItemQuantity()

class ItemType(Enum):
    WEAPON = 0
    TOOL = 1
    QUEST = 2
    ARMOR = 3
    RESOURCE = 4
    MISC = 5
