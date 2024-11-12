import pygame as pg
import numpy as np
import math


# Debug tools
GRAB_MOUSE = True
PROFILE = True

# The width and height of the window the game is displayed on
WIDTH, HEIGHT = 1920, 1080
WIDTH, HEIGHT =  600, 600
CENTRE = (WIDTH//2, HEIGHT//2)
ASPECT_RATIO = WIDTH / HEIGHT

BACKGROUND_COLOR = (32, 32, 32)

# The maximum number of times the main loop can run per second
MAX_FPS = 120

# The size, area and volume of a single chunk
CHUNK_SIZE = 16
CHUNK_AREA = CHUNK_SIZE**2
CHUNK_VOLUME = CHUNK_SIZE**3

# Player variables
PLAYER_SPEED = 1  # Voxels per second
PLAYER_ROTATION_SENSITIVITY = 1
VERTICAL_FOV = 1  # (Radians)

# Clipping planes
NEAR = 0.1
FAR = 1000

# TODO - Vector Class

# Convert a 3d vector to have a length of 1
def normalise(vector):
    magnitude = math.sqrt(vector[0]**2 + vector[1]**2 + vector[2]**2)

    # Avoid edge case of (0, 0, 0) vectors
    if magnitude == 0:
        return (0.0, 0.0, 0.0)

    x = vector[0] / magnitude
    y = vector[1] / magnitude
    z = vector[2] / magnitude

    return [x, y, z]


def add(vector1, vector2):
    x1, y1, z1 = vector1
    x2, y2, z2 = vector2

    return [round(x1+x2,2), round(y1+y2,2), round(z1+z2,2)]

def clamp(n, minn, maxn):
    return max(minn, min(n, maxn))


# Voxel data - used to build meshes
VERTICES = [
    (0, 0, 0),
    (1, 0, 0),
    (1, 1, 0),
    (0, 1, 0),
    (0, 0, 1),
    (1, 0, 1),
    (1, 1, 1),
    (0, 1, 1),
]

FACES = [
    (0, 1, 2, 3),  # Front face
    (4, 5, 6, 7),  # Back face
    (4, 0, 3, 7),  # Left face
    (1, 5, 6, 2),  # Right face
    (4, 5, 1, 0),  # Top face
    (3, 2, 6, 7),  # Bottom face
]

FACE_NORMALS = [
    (0, 0, -1),
    (0, 0, 1),
    (-1, 0, 0),
    (1, 0, 0),
    (0, -1, 0),
    (0, 1, 0),
]