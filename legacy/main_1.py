from random import expovariate
from re import S
from ursina import *
from copy import deepcopy
from math import floor
from ursina.prefabs.file_browser_save import FileBrowserSave
import yaml
import sys
from collections import OrderedDict

# Global Params
SIZE = 20
X_CENTER = int(SIZE / 2)
Y_CENTER = int(SIZE / 2)
CUBE_UNIT = 0.1
X_CUBE = 7  # 1/2 number of full cubes horizontally
Y_CUBE = 4  # 1/2 number of full cubes vertically
EXPORTABLE = True

# YAML Specs
DIRECTION = {
    "south": 0,
    "north": 1,
    "east": 2,
    "west": 3,
}
DIRECTION_INV = {
    0: "south",
    1: "north",
    2: "east",
    3: "west",
}
DIRECTION_PAR = {
    "south": "north",
    "north": "south",
    "west": "east",
    "east": "west",
}
TYPE = {
    "100": "ActiveHinge",
    "010": "ActiveHinge",
    "001": "FixedBrick",
}
ORI = {
    "100": 0,
    "010": 90,
}

MODELS = {
    "CoreComponent": "models/core/core.obj",
    color.blue: "models/brick/brick.obj",
    color.red: "models/hinge/hinge.obj",
    color.green: "models/hinge/hinge.obj",
    "CoreComponent": "models/core/core.obj",
    "FixedBrick": "models/brick/brick.obj",
    "ActiveHinge": "models/hinge/hinge.obj",
}
TEXTURES = {
    "CoreComponent": "models/core/core_na.png",
    color.blue: "models/brick/brick_na.png",
    color.red: "models/hinge/hinge_na.png",
    color.green: "models/hinge/hinge_na.png",
    "CoreComponent": "models/core/core_na.png",
    "FixedBrick": "models/brick/brick_na.png",
    "ActiveHinge": "models/hinge/hinge_na.png",
}

class Inventory(Entity):
    def __init__(self):
        super().__init__(
            parent=camera.ui,
            model="quad",
            scale=(CUBE_UNIT, CUBE_UNIT * 3),
            origin=(0, 0),
            texture="white_cube",
            position=(-CUBE_UNIT * 7, 0),
            texture_scale=(1, 3),
            color=color.gray,
        )
        self.item_parent = Entity(parent=self, scale=(1, 1 / 3))


class GridWorld(Entity):
    def __init__(self, **kwargs):
        super().__init__()

        # create an invisible plane for the mouse to collide with
        self.plane = Entity(
            model="quad",
            color=color.azure,
            origin=(-0.5, -0.5),
            z=10,
            collider="box",
            scale=SIZE,
        )

        # create an invisible plane for the mouse to collide with (change of view)
        self.plane_z = Entity(
            model="quad",
            color=color.azure,
            origin=(-0.5, -0.5),
            z=10,
            collider="box",
            scale=SIZE,
        )

        # make 2d array of entities
        self.grid = [[self.make_cell(x, y) for y in range(SIZE)] for x in range(SIZE)]
        self.cursor = Entity(model=Quad(mode="line"), color=color.blue)

        # Make center head
        self.grid[X_CENTER][Y_CENTER].enabled = True
        self.grid[X_CENTER][Y_CENTER].color = color.yellow
        self.grid[X_CENTER][Y_CENTER].color = color.yellow

        # part inventory
        self.inventory = Inventory()
        up_down = self.make_icon("up/down joint", (0, 1), color.red)
        left_right = self.make_icon("left/right joint", (0, 0), color.green)
        structural = self.make_icon("structural element", (0, -1), color.blue)

        # Add button function
        up_down.on_click = self.change_cursor_red
        left_right.on_click = self.change_cursor_green
        structural.on_click = self.change_cursor_blue

        # Ask To Load YAML File
        self.body_yaml = None
        # self.load_yaml()

        # Add Clear, Save, Load & Toggle View Buttons
        self.clear = Button(
            text="Clear",
            parent=camera.ui,
            model="quad",
            scale=(CUBE_UNIT, CUBE_UNIT / 3),
            origin=(0, 0),
            position=(
                CUBE_UNIT * (0 - X_CUBE),
                CUBE_UNIT * (0 + Y_CUBE) - (CUBE_UNIT / 3),
            ),
            color=color.gray,
            text_origin=(0, 0),
        )
        self.clear.on_click = self.clear_grid

        self.load = Button(
            text="Load",
            parent=camera.ui,
            model="quad",
            scale=(CUBE_UNIT, CUBE_UNIT / 3),
            origin=(0, 0),
            position=(CUBE_UNIT * (0 - X_CUBE), CUBE_UNIT * (0 + Y_CUBE)),
            color=color.gray,
            text_origin=(0, 0),
        )
        self.load.on_click = self.load_yaml

        self.save = Button(
            text="Save",
            parent=camera.ui,
            model="quad",
            scale=(CUBE_UNIT, CUBE_UNIT / 3),
            origin=(0, 0),
            position=(
                CUBE_UNIT * (0 - X_CUBE),
                CUBE_UNIT * (0 + Y_CUBE) + (CUBE_UNIT / 3),
            ),
            color=color.gray,
            text_origin=(0, 0),
        )
        self.save.on_click = self.save_yaml

        self.toggle = Button(
            text="View",
            parent=camera.ui,
            model="quad",
            scale=(CUBE_UNIT, CUBE_UNIT / 3),
            origin=(0, 0),
            position=(CUBE_UNIT * (0 - X_CUBE), CUBE_UNIT * (-1 + Y_CUBE)),
            color=color.gray,
            text_origin=(0, 0),
        )
        self.toggle.on_click = self.toggle_view

    def toggle_view(self):
        global VIEW
        if VIEW == 0:
            camera.rotation = (0, 0, 0)
            camera.position = (10, 10, -10)
            VIEW = 1
        elif VIEW == 1:
            camera.rotation = (0, 90, 0)
            camera.position = (-10, 10, 0)
            VIEW = 2
        elif VIEW == 2:
            camera.rotation = (15, 50, 0)
            camera.position = (-15, 20, -20)
            VIEW = 0

    def save_yaml(self):
        wp = FileBrowserSave(file_type=".yaml")

        # Set Up
        x = X_CENTER
        y = Y_CENTER
        name = "test"
        yaml_out = {"id": name}
        yaml_out["body"] = self.make_section("core", "CoreComponent", "011", 0, None)
        self.get_grid_coloring_init(yaml_out["body"], x, y, ori_p=0)

        wp.data = yaml.dump(yaml_out, sort_keys=False)

        # with open(f"{name}.yaml", "w") as f:
        #     yaml.dump(yaml_out, f, sort_keys=False)

    def load_yaml(self):
        fb = FileBrowser(file_types=("*.yaml"), enabled=True)
        fb.on_submit = self.on_submit

    def set_grid(self, x, y):
        return self.grid[x][y]

    def get_dir(self, x, y, direction):
        if direction == "north":  # North
            points = (x, y + 1)
        if direction == "east":  # East
            points = (x + 1, y)
        if direction == "south":  # South
            points = (x, y - 1)
        if direction == "west":  # West
            points = (x - 1, y)
        return points

    def check_neighbours(self, x, y):
        neighbours = {
            "south": self.get_dir(x, y, "south"),
            "north": self.get_dir(x, y, "north"),
            "east": self.get_dir(x, y, "east"),
            "west": self.get_dir(x, y, "west"),
        }
        # random_generator = random.Random()
        part = {}
        for neighbour in neighbours:
            current = self.set_grid(neighbours[neighbour][0], neighbours[neighbour][1])
            if current.enabled:
                key = DIRECTION[neighbour]
                rel_color = f"{int(current.color.r)}{int(current.color.g)}{int(current.color.b)}"
                part[key] = rel_color
        return part

    def make_section(self, _id, _type, clr, orientation, children=False):
        color_select = {
            "011": {"blue": 0, "green": 1, "red": 1},
            "100": {"blue": 0, "green": 0, "red": 1},
            "010": {"blue": 0, "green": 1, "red": 0},
            "001": {"blue": 1, "green": 0, "red": 0},
        }
        section = {
            "id": _id,
            "type": _type,
            "orientation": orientation,
            "params": color_select[clr],
        }
        if children == False:
            return section
        elif children == None:
            section["children"] = {}
        else:
            section["children"] = children
        return section

    def get_grid_coloring_init(self, yaml, x, y, ori_p, parent=None):
        # YAML Set Up
        children = self.check_neighbours(x, y)
        if len(children) == 0:
            return
        if parent == None:
            for key in children:
                current = children[key]
                _id = f"{TYPE[current]}_{DIRECTION_INV[key].capitalize()}"
                _type = TYPE[current]
                clr = current

                if _type == "FixedBrick":
                    ori = ori_p
                else:
                    ori = ORI[current]

                yaml_selection = self.make_section(_id, _type, clr, ori)
                yaml["children"][key] = yaml_selection
                direction = DIRECTION_INV[key]
                parent = DIRECTION_PAR[direction]
                x_new, y_new = self.get_dir(x, y, direction)
                self.get_grid_coloring_init(
                    yaml["children"][key], x_new, y_new, ori, parent=parent
                )
        else:
            for key in children:
                if key == DIRECTION[parent]:
                    continue
                else:
                    current = children[key]
                    _id = f"{TYPE[current]}_{DIRECTION_INV[key].capitalize()}"
                    _type = TYPE[current]
                    clr = current

                    if _type == "FixedBrick":
                        ori = ori_p
                    else:
                        ori = ORI[current]
                    yaml_selection = self.make_section(_id, _type, clr, ori)
                    try:
                        yaml["children"][key] = yaml_selection
                    except KeyError:
                        yaml["children"] = {}
                        yaml["children"][key] = yaml_selection
                    direction = DIRECTION_INV[key]
                    parent = DIRECTION_PAR[direction]
                    x_new, y_new = self.get_dir(x, y, direction)
                    self.get_grid_coloring_init(
                        yaml["children"][key], x_new, y_new, ori, parent=parent
                    )

    def grid_coloring(self, x_c, y_c, key, orientation, _type, children=False):
        sys.stdout.write("----- NEW SET -----\n")
        sys.stdout.write(f"{key}, {orientation}\n")

        # Get Positon Of New Block
        if key == 0:  # South
            x = x_c
            y = y_c - 1
        elif key == 1:  # North
            x = x_c
            y = y_c + 1
        elif key == 2:  # East
            x = x_c + 1
            y = y_c
        elif key == 3:  # West
            x = x_c - 1
            y = y_c
        else:
            x = X_CENTER
            y = Y_CENTER
        current = self.set_grid(x, y)

        # Assign Correct block Type
        if _type == "CoreComponent" or _type == "Core":
            sys.stdout.write("@ Core\n")
            current.color = color.yellow
            current.model = MODELS[_type]
            current.texture = TEXTURES[_type]
        elif _type == "ActiveHinge":
            sys.stdout.write("@ ActiveHinge\n")
            if orientation == 0:  # TODO: Check
                current.color = color.red
            if orientation == 90:  # TODO: Check
                current.color = color.green
            current.model = MODELS[_type]
            current.texture = TEXTURES[_type]
        elif _type == "FixedBrick":
            sys.stdout.write("@ FixedBrick\n")
            current.color = color.blue
            current.model = MODELS[_type]
            current.texture = TEXTURES[_type]
        current.enabled = True
        sys.stdout.write(f"{x}, {y}\n")

        if children:
            for child in children:
                sys.stdout.write("@ children\n")
                if _type == "ActiveHinge":
                    key_temp = key
                else:
                    key_temp = child
                try:
                    self.grid_coloring(
                        x,
                        y,
                        key=key_temp,
                        orientation=children[child]["orientation"],
                        _type=children[child]["type"],
                        children=children[child]["children"],
                    )
                except KeyError:  # Catch leafs
                    self.grid_coloring(
                        x,
                        y,
                        key=key_temp,
                        orientation=children[child]["orientation"],
                        _type=children[child]["type"],
                        children=False,
                    )

    def on_submit(self, paths):
        for p in paths:
            sys.stdout.write(f"--- {p}\n")
            self.body_yaml = yaml_handler(p)

        sys.stdout.write("======= STARTING YAML LOADING =======\n")
        self.clear_grid(with_center=False)
        yaml = self.body_yaml["body"]
        self.grid_coloring(
            0, 0, key=None, orientation=0, _type=yaml["type"], children=yaml["children"]
        )
        sys.stdout.write("======= ENDING YAML LOADING =======\n")
        sys.stdout.flush()

    def clear_grid(self, with_center=True):
        for y in range(SIZE):
            for x in range(SIZE):
                self.grid[x][y].enabled = False
                self.grid[x][y].color = color.blue
                self.grid[x][y].old_color = None
                self.grid[x][y].texture = "white_cube"
        if with_center:
            # Make center head
            self.grid[X_CENTER][Y_CENTER].enabled = True
            self.grid[X_CENTER][Y_CENTER].color = color.yellow

    def change_cursor_red(self):
        self.cursor.color = color.red

    def change_cursor_green(self):
        self.cursor.color = color.green

    def change_cursor_blue(self):
        self.cursor.color = color.blue

    def make_cell(self, x, y):
        cell = Entity(
            model="cube",
            position=(x, y),
            texture="white_cube",
            color=color.blue,
            enabled=False,
            old_color=None,
        )
        return cell

    def make_icon(self, item, pos, clr):
        icon = Button(
            parent=self.inventory.item_parent,
            scale=(0.9, 0.9),
            model="quad",
            origin=(0, 0),
            position=pos,
            texture="white_cube",
            color=clr,
            z=-0.1,
            disable=True,
        )
        name = item.replace("_", " ").title()
        icon.tooltip = Tooltip(name)
        return icon

    def update(self):
        # Check for wrong parts
        global EXPORTABLE
        EXPORTABLE = True
        for column in self.grid:
            for e in column:
                if [e.x, e.y] == [SIZE / 2, SIZE / 2]:
                    continue
                if e.enabled:
                    state = False
                    try:
                        state = state or self.grid[int(e.x - 1)][int(e.y)].enabled
                        state = state or self.grid[int(e.x + 1)][int(e.y)].enabled
                        state = state or self.grid[int(e.x)][int(e.y - 1)].enabled
                        state = state or self.grid[int(e.x)][int(e.y + 1)].enabled
                    except IndexError:
                        pass
                    if e.color == color.light_gray:
                        self.save.disable()
                    if state == False and e.color != color.light_gray:
                        e.old_color = e.color
                        e.color = color.light_gray
                        e.texture = "broken.png"
                        self.save.disable()
                    if e.color == color.light_gray and state == True:
                        e.color = e.old_color
                        e.old_color = None
                        e.texture = "white_cube"
                        self.save.enable()
                    EXPORTABLE = EXPORTABLE and state
        if held_keys["1"]:
            self.change_cursor_red()
        if held_keys["2"]:
            self.change_cursor_green()
        if held_keys["3"]:
            self.change_cursor_blue()

        if mouse.hovered_entity:
            # round the cursor position
            self.cursor.position = mouse.world_point
            self.cursor.x = round(self.cursor.x, 0)
            self.cursor.y = round(self.cursor.y, 0)

        # Move Camera
        if held_keys["a"]:
            print(camera.x)
            camera.x += CUBE_UNIT
        if held_keys["d"]:
            camera.x -= CUBE_UNIT
        if held_keys["w"]:
            camera.y += CUBE_UNIT
        if held_keys["s"]:
            camera.y -= CUBE_UNIT

        factor = 1 / 50
        camera.z += held_keys["q"] * factor
        camera.z -= held_keys["e"] * factor

        # Rotate Camera
        factor = 1 / 25
        camera.rotation_x += held_keys["h"] * factor
        camera.rotation_x -= held_keys["k"] * factor
        camera.rotation_y += held_keys["u"] * factor
        camera.rotation_y -= held_keys["j"] * factor
        camera.rotation_z += held_keys["y"] * factor
        camera.rotation_z -= held_keys["i"] * factor

    def input(self, key):
        try:  # Out Of Bounds
            current_x = int(self.cursor.x)
            current_y = int(self.cursor.y)
            current = self.grid[current_x][current_y]
        except IndexError:
            pass

        # Process Mouse Presses
        if (3 <= current_x <= 3) and (9 <= current_y <= 11):
            pass  # Skip Inventory
        elif (current_x <= 0) or (current_y <= 0):
            pass  # Skip Buttons
        elif (current_x == X_CENTER) and (current_y == Y_CENTER):
            pass  # Skip Core
        else:
            if key == "left mouse down":
                if current.enabled == False:  # Prevent Duble Press
                    current.color = self.cursor.color
                    current.enabled = True
                    current.model = MODELS[self.cursor.color]
                    current.texture = TEXTURES[self.cursor.color]
            if key == "right mouse down":
                current.enabled = False
                if current.texture.name == "broken.png":
                    current.texture = "white_cube"
                    self.save.enable()


def yaml_handler(path):
    with open(path) as f:
        docs = yaml.load_all(f, Loader=yaml.FullLoader)
        itter = []
        for doc in docs:
            itter.append(doc)
        return itter[0]

if __name__ == "__main__":
    app = Ursina()

    window.title = "Devolve"  # The window title
    window.borderless = False  # Show a border
    window.fullscreen = False  # Do not go Fullscreen
    window.exit_button.visible = False  # Hide in-game red X that loses the window
    window.fps_counter.enabled = True  # Show the FPS (Frames per second) counter
    camera.orthographic = True
    camera.fov = 10
    camera.origin = (X_CENTER, Y_CENTER)
    camera.rotation = (0, 0, 0)
    camera.position = (10, 10, -10)
    VIEW = 1

    GridWorld()

    app.run()
