from item import Item
import random

class Inventory():

    def __init__(self):

        self.INV_SIZE_X = 10
        self.INV_SIZE_Y = 3

        self.items = [[None]*self.INV_SIZE_Y for _ in range(self.INV_SIZE_X)]
        self.hotbar = [None]*self.INV_SIZE_X

        for x in range(len(self.items)):
            for y in range(len(self.items[x])):
                self.items[x][y] = Item("pickaxe")

    def addItem(item):
        for x in range(INV_SIZE_X):
            for y in range(INV_SIZE_Y):
                if self.items[x][y] == None and isinstance(item, Item):
                    self.items[x][y] = item
                    return

    def removeItem(item):
        for x in range(INV_SIZE_X):
            for y in range(INV_SIZE_Y):
                if self.items[x][y] == item:
                    self.items[x][y] = None
                    return

    def placeItem(item, x, y):
        if isinstance(item,Item):
            self.items[x][y] = item

    def placeItemInHotbar(item, index):
        if isinstance(item,Item):
            hotbar[index] = item

    def addItemToHotbar(item):
        for x in range(INV_SIZE_X):
            if hotbar[x] == None:
                hotbar[x] = item
                return
