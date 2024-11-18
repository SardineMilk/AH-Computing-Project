from settings import *

from player import Player
from world import World

if PROFILE:
    import profiler
    profiler.profiler().start(True)

class VoxelEngine:
    def __init__(self):
        # Initialise the pygame window
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))

        # Initialise the player class
        self.player = Player([0, 0, 0], [0, 0, 0])

        # Initialise the world
        self.world = World("file_name")

        # Initialise the clock - used for fps and movement
        self.clock = pg.time.Clock()

        # Hide and lock the mouse
        if GRAB_MOUSE:
            pg.mouse.set_visible(False)
            pg.event.set_grab(True)  # Prevents mouse from moving

        self.running = True

    def handleEvents(self):
        # This function will (probably) connect to the database
        # Process the event queue
        # Calling pg.event.get() here means later input handling will work without additional overhead
        for event in pg.event.get():
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.running = False

        # Get the keyboard and mouse data
        self.keys = pg.key.get_pressed()
        self.relative_mouse_movement = pg.mouse.get_rel()
        self.mouse_pressed = pg.mouse.get_pressed()

    def update(self):
        # Update all time related variables
        self.delta = self.clock.tick()  # Time since last frams
        self.fps = self.clock.get_fps()
        self.time = pg.time.get_ticks() * 0.001  # Program's runtime in seconds

        # Update player
        self.player.update(self.keys, self.relative_mouse_movement, self.mouse_pressed, self.delta)  # This should be before world so the matrices get updated/generated

        # Update world
        self.world.update(self.player.position, self.player.look_pos, self.player.look_type)

    def render(self):
        # Clear the screen
        self.screen.fill(BACKGROUND_COLOR)
        # Display voxel faces
        
        
        faces = self.world.mesh
        
        #[pg.gfxdraw.filled_polygon(self.screen, shape, color) for shape, color in faces]  # Slower
        if faces != None:
            [pg.draw.polygon(self.screen, (0, 127, 127), shape) for (shape, color) in faces]

        # Display HUD
        #print(self.player.position.position().round(1), "   ", self.player.rotation.position().round(1), "  ", round(self.fps, 2), "   ", len(self.world.chunks))  
        pg.display.flip()

    def run(self):
        # Main game loop
        while self.running:
            # Handle inputs - Mouse + Keyboard
            self.handleEvents()
            # Update the matrices, movement, sort mesh etc
            self.update()
            # Render the mesh
            self.render()
            # Cap the fps
            self.clock.tick(MAX_FPS)
        # Close the window if the player quits
        pg.quit()


# The main function of the next line is to stop the code from running if the file is imported as a module
# However, it also makes 'game' a local variable instead of global
# Thus means python can use STORE_FAST instead of STORE_NAME in the bytecode, giving a minor performance increase
if __name__ == "__main__":
    game = VoxelEngine()
    game.run()

