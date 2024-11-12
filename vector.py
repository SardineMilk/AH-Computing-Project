from settings import *

class Vector:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

        self.length = math.sqrt(self.x**2 + self.y**2 + self.z**2)
    
    def position(self):
        return [self.x, self.y, self.z]
    
    def rotate(self, pitch, yaw, roll):
        pass