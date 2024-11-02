import pygame as pg
import numpy as np


# The width and height of the window the game is displayed on
WIDTH, HEIGHT = 1920, 1080
CENTRE = (WIDTH//2, HEIGHT//2)

# The maximum number of times the main loop can run per second
MAX_FPS = 120

CHUNK_SIZE = 16
CHUNK_AREA = CHUNK_SIZE**2
CHUNK_VOLUME = CHUNK_SIZE**3