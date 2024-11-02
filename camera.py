from settings import *

class Camera:
    def __init__(self, position, rotation):
        self.position = position
        self.rotation = rotation

        # The projection matrix doesn't change, so it is calculated once at runtime
        self.projection_matrix = self.generateProjectionMatrix()


    def updateCameraMatrix(self):
        # The view matrix changes each time the postition or rotation changes,
        # So we recalculate it every frame
        self.view_matrix = self.generateViewMatrix()

        self.cameraMatrix = self.viewMatrix * self.projectionMatrix


    def generateViewMatrix(self):
        # Multiply the mesh by this to rotate and translate it from world space to view space
        # i.e. first person perspective

        return


    def generateProjectionMatrix(self):
        # Multiply the mesh by this to project it onto the screen - 3d to 2d
        # It is a 4*4 matrix, which means it is not destructive - You can multiply by the inverse to reverse the process

        # Initialise the matrix
        projection_matrix = np.zeros((4, 4))

        # Determine half-height/width of near plane
        half_height = math.tan(VERTICAL_FOV/2) * NEAR
        half_width = half_height * ASPECT_RATIO

        projection_matrix[0][0] = NEAR / half_width  # Controls x scaling 
        projection_matrix[1][1] = NEAR / half_height  # Controls y scaling
        projection_matrix[2][2] = (FAR + NEAR) / (FAR - NEAR)  # Defines the depth range. Maps the [NEAR, FAR] range to [-1, 1]
        projection_matrix[2][3] = (2 * FAR * NEAR) / (FAR - NEAR)  # Controls z scaling factor
        projection_matrix[3][2] = -1  # Ensure perspective divide happens

        return projection_matrix