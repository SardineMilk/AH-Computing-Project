from settings import *
from chunk import VoxelChunk


class World:
    def __init__(self, world_name):
        self.world_name = world_name

        # Flatpacked array of Chunk objects
        self.chunks = []

        # Mesh of faces - (((x1,y1,z1), (x2,y2,z2), (x3,y3,z2), (x4,y4,z3)), (r, g, b))
        self.mesh = []

    def update(self, player_pos, altered_voxel_pos, altered_voxel_type):
        # Load new chunks if needed
        self.__updateRenderedChunks(player_pos)

        # Place/Remove voxel if needed
        if altered_voxel_type != None:
            altered_chunk_pos = self.__worldToLocal(altered_voxel_pos.position())[0]  # We only need the chunk, not the local pos
            altered_chunk_x, altered_chunk_y, altered_chunk_z = altered_chunk_pos
            # If chunk isn't loaded, load it
            # Since we update adjacent chunks later, we need to check if they are loaded too
            # We could check if they are loaded while updating, but that would create an edge case leading to saved chunks being loaded with holes in the mesh
            if self.__getChunkIndex((altered_chunk_x, altered_chunk_y, altered_chunk_z)) == None:
                self.__loadChunk((altered_chunk_x, altered_chunk_y, altered_chunk_z))
            if self.__getChunkIndex((altered_chunk_x+1, altered_chunk_y, altered_chunk_z)) == None:  # +x
                self.__loadChunk((altered_chunk_x+1, altered_chunk_y, altered_chunk_z))  
            if self.__getChunkIndex((altered_chunk_x-1, altered_chunk_y, altered_chunk_z)) == None:  # -x
                self.__loadChunk((altered_chunk_x-1, altered_chunk_y, altered_chunk_z))  
            if self.__getChunkIndex((altered_chunk_x, altered_chunk_y+1, altered_chunk_z)) == None:  # +y
                self.__loadChunk((altered_chunk_x, altered_chunk_y+1, altered_chunk_z))
            if self.__getChunkIndex((altered_chunk_x, altered_chunk_y-1, altered_chunk_z)) == None:  # -y
                self.__loadChunk((altered_chunk_x, altered_chunk_y-1, altered_chunk_z))
            if self.__getChunkIndex((altered_chunk_x, altered_chunk_y, altered_chunk_z+1)) == None:  # +z
                self.__loadChunk((altered_chunk_x, altered_chunk_y, altered_chunk_z+1))
            if self.__getChunkIndex((altered_chunk_x, altered_chunk_y, altered_chunk_z-1)) == None:  # -z  
                self.__loadChunk((altered_chunk_x, altered_chunk_y, altered_chunk_z-1))         

            # Alter voxel
            self.setVoxel(altered_voxel_pos.position(), altered_voxel_type)
            #print(self.__getChunk((altered_chunk_x, altered_chunk_y, altered_chunk_z)).voxels)
            #print(self.__getChunk((altered_chunk_x, altered_chunk_y, altered_chunk_z)).getVoxel((0, 0, 0)))
            # Recreate mesh in altered chunks
            # We need to update all adjacent chunks as well to prevent holes in the mesh if you remove a voxel at the edge of a chunk
            self.getChunk((altered_chunk_x, altered_chunk_y, altered_chunk_z)).updateMesh()
            self.getChunk((altered_chunk_x+1, altered_chunk_y, altered_chunk_z)).updateMesh()  # +x
            self.getChunk((altered_chunk_x-1, altered_chunk_y, altered_chunk_z)).updateMesh()  # -x
            self.getChunk((altered_chunk_x, altered_chunk_y+1, altered_chunk_z)).updateMesh()  # +y
            self.getChunk((altered_chunk_x, altered_chunk_y-1, altered_chunk_z)).updateMesh()  # -y
            self.getChunk((altered_chunk_x, altered_chunk_y, altered_chunk_z+1)).updateMesh()  # +z
            self.getChunk((altered_chunk_x, altered_chunk_y, altered_chunk_z-1)).updateMesh()  # -z

        
    def __updateRenderedChunks(self, player_pos):
        #TODO add unloading
        for i in range(RENDER_DISTANCE ** 3):
            # Generate an [x, y, z] index in a cube pattern
            x = i % RENDER_DISTANCE
            y = (i // RENDER_DISTANCE) % RENDER_DISTANCE
            z =i // RENDER_DISTANCE ** 2

            # Shift so chunks generate centred on the player
            x = int(player_pos.x//CHUNK_SIZE + x)
            y = int(player_pos.y//CHUNK_SIZE + y)
            z = int(player_pos.z//CHUNK_SIZE + z)

            loaded_chunk_position = [x, y, z]
            if self.__getChunkIndex(loaded_chunk_position) == None:
                self.__loadChunk(loaded_chunk_position)
                #print(f"Loaded {loaded_chunk_position}")

    def getVoxel(self, position):
        # Using a world position, return the local position
        chunk_position, local_position = self.__worldToLocal(position)
        chunk_data = self.__getChunkData(chunk_position)
        return chunk_data.getVoxel(local_position)
    
    def setVoxel(self, position, type):
        # Set the type of a voxel at a specific world position
        # Get the chunk object we need to change
        chunk_position, local_position = self.__worldToLocal(position)
        chunk = self.getChunk(chunk_position)
        # Change the type of the voxel
        chunk.setVoxel(local_position, type)

    def __getChunkData(self, position):
        # 3d to flatpack
        chunk_index = self.__getChunkIndex(position)
        return self.chunks[chunk_index]

    def __loadChunk(self, position):
        # Check if in file
        # Else:
        self.chunks.append(VoxelChunk(list(position), np.zeros([16,16,16], dtype=int)))

    def __worldToLocal(self, position) -> tuple[list[int, int, int], list[int, int, int]]:
        # Convert a world position to a local position
        # Position of the chunk in 3d space
        chunk_index = [position[0] // CHUNK_SIZE, position[1] // CHUNK_SIZE, position[2] // CHUNK_SIZE]
        # Index of the voxel within the chunk
        local_index = [position[0] % CHUNK_SIZE, position[1] % CHUNK_SIZE, position[2] % CHUNK_SIZE]

        return chunk_index, local_index
    
    def __getChunkIndex(self, position) -> int|None:
        # From a chunk position, get the 
        # Index of the chunk in the array of loaded chunks
        for index, chunk in enumerate(self.chunks):
            if chunk.position == list(position):  
                return index
        return None

    def getChunk(self, position) -> VoxelChunk:
        return self.chunks[self.__getChunkIndex(position)]