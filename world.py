from settings import *


class World:
    def __init__(self, world_name):
        self.world_name = world_name
        pass

    def update(self):
        pass

    def getVoxel(self, position):
        pass

    def setVoxel(self, position, type):
        pass

    def __getChunkData(self, index):
        pass

    def __loadChunk(self, index):
        pass