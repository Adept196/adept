import os.path

import pygame

from buffalo import utils
from buffalo.label import Label

import tile
import mapManager
import biome


"""
A Chunk is a data structure
that holds tiles.
"""
class Chunk:

    """
    CHUNK_HEIGHT and CHUNK_WIDTH represent
    the size, in tiles, of each Chunk
    """
    CHUNK_HEIGHT, CHUNK_WIDTH = 8, 8
    TILE_SIZE                 = tile.Tile.TILE_SIZE

    LOADED_SURFACES = dict()

    def __init__(self, x, y, from_other_thread=False):
        """
        This is the Chunk constructor.
        It creates a Chunk at the coordinates (<x>, <y>).
        <x> and <y> are positive or negative integers.

        self.pos  - a 2-tuple that stores the coordinates of the Chunk
        self.defs - a dictionary that stores definitions of tiles
                    self.defs' keys are specified in the file.
                    Each key maps to an RGBA 4-tuple, for now, at least.
        self.data - a two-dimensional array of strings
                    Each string is a key, which, when plugged into the
                    dictionary self.defs, returns an RGBA 4-tuple
        """
        self.path = None
        for m in mapManager.MapManager.maps:
            search_path_list = m.pathlist + ["chunks", "{0},{1}.chunk".format(x, y)]
            search_path_string = os.path.join(*search_path_list)
            if search_path_string in m.chunk_files:
                self.pathlist = search_path_list
                self.path = search_path_string
                break
        self.pos = x, y
        self.defs = dict()
        self.data = [["" for _x in range(Chunk.CHUNK_WIDTH)] for _y in range(Chunk.CHUNK_HEIGHT)]
        self.tiles = list()
        if self.path is None:
            self.data = mapGenerator.MapGenerator.GenerateChunk(0, self.pos[0], self.pos[1])
            self.defs = biome.Biome.GenerateBiomeDefs()
            self.toFile()
        self.fromFile(x, y)
        if not from_other_thread:
            self.create_and_render_surface()

    def create_and_render_surface(self):
#        self.label = Label(
#            (5,5),
#            str((self.pos[0], self.pos[1])),
#            font="default36",
#            color=(0,0,0,255)
#        )
        self.surface = utils.empty_surface(
            (Chunk.TILE_SIZE * Chunk.CHUNK_WIDTH, Chunk.TILE_SIZE * Chunk.CHUNK_HEIGHT)
        )
        self.render()

    def create_surface(self):
        self.surface = utils.empty_surface(
            (Chunk.TILE_SIZE * Chunk.CHUNK_WIDTH, Chunk.TILE_SIZE * Chunk.CHUNK_HEIGHT)
        )
        
    @staticmethod
    def loadSurfaceForId(_id):
        if _id in Chunk.LOADED_SURFACES.keys():
            return Chunk.LOADED_SURFACES[_id]
        IMG_FILE = os.path.join(os.path.join(*list(['assets','terrain'] + [str(_id) + ".png"])))
        try:
            surface = pygame.image.load(IMG_FILE)
            Chunk.LOADED_SURFACES[_id] = surface
            return surface
        except Exception as e:
            print("Error: Chunk texture for item \"" + str(_id) + "\" does not exist.")
            print(e)
            IMG_FILE = os.path.join(os.path.join(*list(['assets'] + ["error.png"])))
            surface = pygame.image.load(IMG_FILE)
            Chunk.LOADED_SURFACES[_id] = surface
            return surface

    def generateDataAndDefs(self):
        x,y = self.pos
        self.data = mapGenerator.MapGenerator.GenerateChunk(self.seed,x,y)
        self.defs = biome.Biome.GenerateBiomeDefs()
        self.toFile()

    def fromFile(self, x, y):
        """
        This method loads a chunk from a file.
        The chunk is specified by coordinates, <x> and <y>,
        which are positive or negative integers.
        """

        if self.path is None:
            return

        # Be sure the URL points to a file before trying to open it
        if not os.path.isfile(self.path):
            print("Could not load chunk in path '" + self.path + "'.")
            return
        
        with open(self.path,"r") as chunkFile:
            # Keep track of which row of data we want to fill
            row = 0

            for line in chunkFile:
                stripped = line.strip()
                # If the line isn't blank
                if stripped:
                    splitted = stripped.split()
                    if len(splitted) >= 4 and splitted[0] == "define": # If the definition is formatted correctly

                        # Then assign map the value to the specified key in self.defs
                        # This is an RGBA 4-tuple
                        self.defs[splitted[1]] = (
                            int("0x"+splitted[3][1:3],16), # R
                            int("0x"+splitted[3][3:5],16), # G
                            int("0x"+splitted[3][5:7],16), # B
                            255,                           # A = 255 = fully opaque
                        )
                        # This is RGBA and not RGB because Buffalo is written to handle transparency
                        # Pygame suffers huge performance losses when converting between RGB and RGBA
                        # surface types. If everything is RGBA then Pygame never has to convert surface
                        # types and thus does not suffer from these performance losses.

                    else: # If we aren't looking at a correctly formatted definition

                        # Then interpret the line as chunk data
                        for col, key in enumerate(splitted):
                            if col < Chunk.CHUNK_WIDTH and row < Chunk.CHUNK_HEIGHT:
                                self.data[row][col] = key
                                self.tiles.append(
                                    tile.Tile(
                                        pos=(col * Chunk.TILE_SIZE, row * Chunk.TILE_SIZE, 0),
                                        base_color=(self.defs[key]),
                                        type_id=key,
                                        use_images=True,
                                    )
                                )

                        row += 1 # And remember to keep track of the row!
        #print str(self.pos)
        #print self.data

    def render(self):
#        for y, row in enumerate(self.data):
#            for x, col in enumerate(row):
#                if col in self.defs.keys():
                    #Image/Texture Based Rendering
                    #self.surface.blit(
                    #    Chunk.loadSurfaceForId(col),
                    #    (x * Chunk.TILE_SIZE, y * Chunk.TILE_SIZE)
                    #)

                    #Color Based Rendering
                    #self.surface.fill(
                    #    self.defs[col],
                    #    pygame.Rect(
                    #        (x * Chunk.TILE_SIZE, y * Chunk.TILE_SIZE),
                    #        (Chunk.TILE_SIZE, Chunk.TILE_SIZE),
                    #    )
                    #)
        for _tile_ in self.tiles:
            _tile_.blit(self.surface)
#        self.label.blit(self.surface)

    def blit(self, dest, pos):
        dest.blit( self.surface, pos )

    def toFile(self):
        # TODO
        # UPDATE THIS METHOD
        # USE self.path AND OTHER STUFF
        """
        This method saves a chunk to a file.
        This should only be called when a map has been updated at runtime,
        as the function overwrites previous chunk data.
        """

        # Create a URL that's dependent on platform
        LOAD_PATH = mapManager.MapManager.BASE_PATH + [mapManager.MapManager.activeMap.name, "chunks"]
        url = os.path.join(*list(LOAD_PATH + [str(self.pos[0]) + "," + str(self.pos[1]) + ".chunk"]))

        #Opens file in overwrite / file creation mode
        with open(url,"w+") as chunkFile:
            #Iterate through the tile definition dictionary
            for key, value in self.defs.items():
                #Start the definition line with the keyword and key
                chunkFile.write("define " + str(key) + " as #")

                #Reassemble the RGB integers to hex strings
                #IMPORTANT: Skipping last element because transparency is not currently saved
                for i in range(0,3):
                    RGBString = hex(value[i])[2:]
                    #Appending 0 to hex values less than 0x10 to maintain 2-character length per RGB
                    if(len(RGBString) < 2):
                        RGBString = "0" + RGBString
                    chunkFile.write(str(RGBString))
                chunkFile.write("\n") #New line after each definition

            #Iterate through the 2-dimensional list containing chunk data
            for row in self.data:
                for col in row:
                    #At each data point: write data, add white space
                    chunkFile.write(str(col) + " ")
                chunkFile.write("\n") #New line at end of each row

        self.path = url

import mapGenerator
