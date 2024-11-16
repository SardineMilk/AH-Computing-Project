from settings import *
from camera import Camera
from pygame.locals import *

class Player(Camera):
    def update(self, keys, mouse_movement, mouse_pressed, delta):
        # Update the position/rotation using the input values
        self.__rotate(mouse_movement, delta)
        self.__move(keys, delta)
        self.__calculateLookPosAndType(mouse_pressed)

        # Update the matrices with the new values
        self._updateCameraMatrix()
    
    def __move(self, keys, delta):
        speed = PLAYER_SPEED
        movement_vector = Vector((0, 0, 0))  #x, y, z

        # Right
        if keys[pg.K_d]:
            movement_vector.x += speed
        # Left
        if keys[pg.K_a]:
            movement_vector.x -= speed
        # Up
        if keys[pg.K_SPACE]:
            movement_vector.y += speed
        # Down
        if keys[pg.K_LSHIFT]:
            movement_vector.y -= speed
        # Forward
        if keys[pg.K_w]:
            movement_vector.z += speed
        # Back
        if keys[pg.K_s]:
            movement_vector.z -= speed
        
        # Normalise the vector so moving diagonally isn't faster
        movement_vector.normalise()
        
        # Rotate the vector so moving forward always moves you 'forward' from your perspective
        movement_vector.rotate(self.rotation.x, self.rotation.y, self.rotation.z)

        self.position = self.position + movement_vector

    def __rotate(self, mouse_movement, delta):
        yaw   = mouse_movement[0] * PLAYER_ROTATION_SENSITIVITY 
        pitch = mouse_movement[1] * PLAYER_ROTATION_SENSITIVITY 

        rotation_vector = Vector((yaw, pitch, 0))
        # Add the rotation vector to the player rotation 
        self.rotation = self.rotation + rotation_vector
        # Clamp the pitch to directly up/down
        self.rotation.y = clamp(self.rotation.y, -90, 90)
    
    def __calculateLookPosAndType(self, mouse_pressed):
        self.look_pos = Vector((0, 0, 0))
        self.held_voxel = 1

        if mouse_pressed[0]:  # Left Click
            self.look_type = 0
        elif mouse_pressed[2]:  # Right Click
            self.look_type = self.held_voxel
        else:
            self.look_type = None