from settings import *


class VoxelChunk:
    def __init__(self, position, voxels):
        self.position = position  # The position of the chunk [x, y, z]
        self.voxels = voxels  # The voxel data of the chunk. [16*16*16] array
        self.mesh = self.updateMesh()
  
    def getVoxel(self, position):
        x, y, z = position

        # Range check - is position in bounds of the chunk
        if (0 < x or x > CHUNK_SIZE - 1 or 
            0 < y or y > CHUNK_SIZE - 1 or
            0 < z or z > CHUNK_SIZE - 1):
            print(f"Index {position} is out of range of chunk")
            return 0

        return int(self.voxels[x, y, z])

    def setVoxel(self, position, type):
        x, y, z = position
        # Range check - is position in bounds of the chunk
        if (0 < x or x > CHUNK_SIZE - 1 or 
            0 < y or y > CHUNK_SIZE - 1 or
            0 < z or z > CHUNK_SIZE - 1):
            print(f"Index {position} is out of range of chunk")
        self.voxels[x, y, z] = type

    def loadChunkData(self):
        # Open file: world_name/chunk_index.txt
        # Change from flat to 3d format
        # Set data
        pass

    def updateMesh(self):
        # Sieve transparent voxels
        filtered_voxels = np.argwhere(self.voxels != 0)  # TODO - Support multiple transparent voxels


        self.mesh = []
        for voxel_pos in filtered_voxels:
            for face_index, face_normal in enumerate(FACE_NORMALS):
                # Interior Face Culling
                check_pos = Vector(voxel_pos) + face_normal
                if self.voxels[check_pos.x, check_pos.y, check_pos.z] == 0:
                    voxel_type = self.voxels[voxel_pos[0], voxel_pos[1], voxel_pos[2]]
                    face = [VERTICES[i].position()[0:2] for i in FACES[face_index]]
                    self.mesh.append((tuple(face), voxel_type))
        # voxel_color = voxel_types[voxel_type]
        # Greedy Meshing
