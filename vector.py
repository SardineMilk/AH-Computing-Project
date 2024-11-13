from settings import *

class Vector:
    def __init__(self, position):
        self.x = position[0]
        self.y = position[1]
        self.z = position[2]

    def length(self):
        return math.sqrt(self.x**2 + self.y**2 + self.z**2)
    
    def position(self):
        return np.array([self.x, self.y, self.z])
    
    def rotate(self, pitch, yaw, roll):
        # Convert angles from degrees to radians
        pitch = np.radians(pitch)
        yaw = np.radians(yaw)
        roll = np.radians(roll)

        # Define the rotation matrices
        yaw_matrix = np.array([
            [np.cos(yaw), 0, np.sin(yaw)],
            [0, 1, 0],
            [-np.sin(yaw), 0, np.cos(yaw)]
        ])

        pitch_matrix = np.array([
            [1, 0, 0],
            [0, np.cos(pitch), -np.sin(pitch)],
            [0, np.sin(pitch), np.cos(pitch)]
        ])

        roll_matrix = np.array([
            [np.cos(roll), -np.sin(roll), 0],
            [np.sin(roll), np.cos(roll), 0],
            [0, 0, 1]
        ])

        # Combine the matrices 
        # Rotation matrices are not commutative, so the order we multiply them in matters
        rotation_matrix = pitch_matrix @ yaw_matrix
        # Apply the matrix to the vector
        rotated =  self.position() @ rotation_matrix

        self.x = rotated[0]
        self.y = rotated[1]
        self.z = rotated[2]


    def __add__(self, other):
        # If the thing you are adding isn't a vector, return NotImplemented
        if not isinstance(other, Vector):
            return NotImplemented
        
        return Vector((self.x + other.x, self.y + other.y, self.z + other.z))
    
    def __sub__(self, other):
        # If the thing you are adding isn't a vector, return NotImplemented
        if not isinstance(other, Vector):
            return NotImplemented
        
        return Vector((self.x - other.x, self.y - other.y, self.z - other.z))
    
    def __iadd__(self, other):
        # If the thing you are adding isn't a vector, return NotImplemented
        if not isinstance(other, Vector):
            return NotImplemented
        
        self.x += other.x
        self.y += other.y
        self.z += other.z

    def __isub__(self, other):
        # If the thing you are adding isn't a vector, return NotImplemented
        if not isinstance(other, Vector):
            return NotImplemented
        
        self.x -= other.x
        self.y -= other.y
        self.z -= other.z

    def normalise(self):
        # Convert a 3d vector to have a length of 1
        
        # Avoid edge case of (0, 0, 0) vectors
        if self.length() == 0:
            self.x = 0
            self.y = 0
            self.z = 0
        else:
            self.x = self.x / self.length()
            self.y = self.y / self.length()
            self.z = self.z / self.length()

    def round(self, length):
        self.x = round(self.x, length)
        self.y = round(self.y, length)
        self.z = round(self.z, length)
