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
        # Convert angles from degrees to radians
        pitch = np.radians(pitch)
        yaw = np.radians(yaw)
        roll = np.radians(roll)

        # Define the rotation matrices
        pitch_matrix = np.array([
            [1, 0, 0],
            [0, np.cos(pitch), -np.sin(pitch)],
            [0, np.sin(pitch), np.cos(pitch)]
        ])

        yaw_matrix = np.array([
            [np.cos(yaw), 0, np.sin(yaw)],
            [0, 1, 0],
            [-np.sin(yaw), 0, np.cos(yaw)]
        ])

        roll_matrix = np.array([
            [np.cos(roll), -np.sin(roll), 0],
            [np.sin(roll), np.cos(roll), 0],
            [0, 0, 1]
        ])

        # Combine the matrices 
        # Rotation matrices are not commutative, so the order we multiply them in matters
        rotation_matrix = roll_matrix @ yaw_matrix @ pitch_matrix
        # Apply the matrix to the vector
        return self * rotation_matrix

    def __add__(self, other):
        # If the thing you are adding isn't a vector, return NotImplemented
        if not isinstance(other, Vector):
            return NotImplemented
        
        return Vector(self.x + other.x, self.y + other.y, self.z + other.z)
    
    def __iadd__(self, other):
        # If the thing you are adding isn't a vector, return NotImplemented
        if not isinstance(other, Vector):
            return NotImplemented
        
        self.x += other.x
        self.y += other.y
        self.z += other.z
        self.length = math.sqrt(self.x**2 + self.y**2 + self.z**2)

    def normalise(self):
        # Convert a 3d vector to have a length of 1
        
        # Avoid edge case of (0, 0, 0) vectors
        if self.length == 0:
            return (0.0, 0.0, 0.0)

        x = self.x / self.length
        y = self.y / self.length
        z = self.z / self.length
