from settings import *
from camera import Camera
from pygame.locals import *

class Player(Camera):
    def update(self, keys, mouse_movement, delta):
        # Update the position/rotation using the input values
        self.__rotate(mouse_movement, delta)
        self.__move(keys, delta)

        # Update the matrices with the new values
        self._updateCameraMatrix()
    
    def __move(self, keys, delta):
        speed = PLAYER_SPEED * delta
        movement_vector = [0, 0, 0]  #x, y, z

        # x
        if keys[pg.K_d]:
            movement_vector[0] += speed
        if keys[pg.K_a]:
            movement_vector[0] -= speed
        # y
        if keys[pg.K_SPACE]:
            movement_vector[1] += speed
        if keys[pg.K_LSHIFT]:
            movement_vector[1] -= speed
        # z
        if keys[pg.K_w]:
            movement_vector[2] += speed
        if keys[pg.K_s]:
            movement_vector[2] -= speed
        
        movement_vector = normalise(movement_vector)
        self.position = add(self.position, movement_vector)

    def __rotate(self, mouse_movement, delta):
        yaw   = mouse_movement[0] * PLAYER_ROTATION_SENSITIVITY * delta
        pitch = mouse_movement[1] * PLAYER_ROTATION_SENSITIVITY * delta

        rotation_vector = [yaw, pitch, 0]
        self.rotation = add(self.rotation, rotation_vector)

        # Clamp the pitch to directly up/down
        self.rotation[1] = clamp(self.rotation[1], -90, 90)
        