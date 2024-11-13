from settings import *

class Camera:
    def __init__(self, position, rotation):
        self.position = Vector(position)
        self.rotation = Vector(rotation)

        # The projection matrix doesn't change, so it is calculated once at runtime
        self.__generateProjectionMatrix()

    def _updateCameraMatrix(self):
        # The view matrix changes each time the postition or rotation changes,
        # So we recalculate it every frame
        self.__generateViewMatrix()

        self.cameraMatrix = self.__projection_matrix  # @ self.view_matrix

    def __generateViewMatrix(self):
        # Multiply the mesh by this to rotate and translate it from world space to view space
        # i.e. first person perspective
        pass

    def __generateProjectionMatrix(self):
        # Multiply the mesh by this then divide by w' to project it onto the screen - 3d to 2d
        # It is a 4*4 matrix, which means it is not destructive - You can reverse the process to reverse the process

        # [x, y, z, 1] @ [matrix] = [x', y', z', w']

        # Initialise the matrix
        self.__projection_matrix = np.zeros((4, 4))

        # Determine half-height/width of near plane
        half_height = math.tan(VERTICAL_FOV/2) * NEAR
        half_width = half_height * ASPECT_RATIO

        self.__projection_matrix[0][0] = NEAR / half_width  # Controls x scaling 
        self.__projection_matrix[1][1] = NEAR / half_height  # Controls y scaling
        self.__projection_matrix[2][2] = (FAR + NEAR) / (FAR - NEAR)  # Defines the depth range. Maps the [NEAR, FAR] range to [-1, 1]
        self.__projection_matrix[2][3] = (2 * FAR * NEAR) / (FAR - NEAR)  # Controls z scaling factor
        self.__projection_matrix[3][2] = -1  # Ensure perspective divide happens: w' = -z

        # Divide (x', y', z') by w' manually in a seperate step
        