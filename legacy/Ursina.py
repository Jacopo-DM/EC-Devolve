from ursina import *  # Import the ursina engine
import random                           # Import the random library

random_generator = random.Random()      # Create a random number generator

app = Ursina()  # Initialise your Ursina app

window.title = "Devolve"  # The window title
window.borderless = False  # Show a border
window.fullscreen = False  # Do not go Fullscreen
window.exit_button.visible = (
    False  # Do not show the in-game red X that loses the window
)
window.fps_counter.enabled = True  # Show the FPS (Frames per second) counter

def update():
    pass

def move_dir(obj, dir):
    obj.x += dir.x
    obj.y += dir.y
    obj.z += dir.z

def input(key):
    if key == 'space':
        print(c2.forward)
        print(c2.back)
        print(c2.right)
        print(c2.left)
        print(c2.up)
        print(c2.down)
    if key == 'w':
        move_dir(c2, c2.forward)
    if key == 's':
        move_dir(c2, c2.back)
    if key == 'd':
        move_dir(c2, c2.right)
    if key == 'a':
        move_dir(c2, c2.left)
        print(c2.left)
    if key == 'q':
        move_dir(c2, c2.up)
    if key == 'z':
        move_dir(c2, c2.down)
    if key == 'e':
        c2.rotation_z += 45
    if key == 'c':
        c2.rotation_z -= 45

c2 = Entity(model='cube', color=color.blue, scale=(1,1,1), texture = 'white_cube')

# forward             # get forward direction.
# back                # get backwards direction.
# right               # get right direction.
# left                # get left direction.
# up                  # get up direction.
# down                # get down direction.

EditorCamera()
app.run()  # Run the app
