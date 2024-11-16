from chunk import VoxelChunk
import numpy as np
chunk = VoxelChunk((0, 0, 0), np.zeros([16,16,16], dtype=int))

print(chunk.voxels[0, 0, 0])
print(chunk.getVoxel((0, 0, 0)))

chunk.setVoxel((0, 0, 0), 1)

print(chunk.voxels[0, 0, 0])
print(chunk.getVoxel((0, 0, 0)))