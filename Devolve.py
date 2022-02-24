#!/usr/bin/env python3

""" Code Info
Author:     Jacopo Di Matteo
Date:       23.02.2022

This code was produced as part of 'advanced research project' for the
Evolutionary Computing master course at the Vrije Universiteit.

This script provides a visual interface to edit and create robots compatible with the
revolve evolutionary simulation suite. The robot descriptions are printed out in YAML
format, which can these can be directly used in revolve experiments.

It was built for simplicity of transportation, rather than maintenance,
therefore it is a single monolithic file that includes all the required components to run.

Requirements:
    $ pip install -r requirements.txt

    or copy the conda environment:
    $ conda env create -f environment.yml

Example:
    $ python Devolve.py

TODO:
- [ ] Undo/Redo

This code is provided 'As Is'.
"""

# =============================== Imports ===================================== #
# Thirdparty
from ursina import *
from ursina.prefabs.file_browser_save import FileBrowserSave
import yaml

# =============================== Constants ===================================== #
# Global Constants (Needed For Intellisense And Extendability)
ID = "id"
BODY = "body"
TYPE = "type"
PARAMS = "params"
BLUE = "blue"
GREEN = "green"
RED = "red"
ORIENTATION = "orientation"
CHILDREN = "children"
CORE = "CoreComponent"
HINGE = "ActiveHinge"
BRICK = "FixedBrick"

"""string: module level constants, YAML headers definitions
Needed for future proof, as the naming choice for Revolve is arbitrary
"""

ASSETS = {
    CORE: "assets/core/core",
    BRICK: "assets/brick/brick",
    HINGE: "assets/hinge/hinge",
}
"""dict: module level constants
Dictionary that define path to model asssets
"""

COLORS = {
    0: {
        CORE: Color(1, 1, 1, 1),  # White
        BRICK: Color(1, 0.278, 0.122, 1),  # 1F47FF
        HINGE: Color(0.439, 0, 1, 1),  # 94FF00
    },
    90: {
        BRICK: Color(0, 0.706, 1, 1),  # 1F47FF
        HINGE: Color(0, 1, 0.58, 1),  # FF0070
    },
}
"""dict: module level constants
Dictionary that defines color of different part types
"""

CORE_CHILD_POS = {
    0: (-1, 0, 0),
    1: (1, 0, 0),
    2: (0, -1, 0),
    3: (0, 1, 0),
}

CORE_CHILD_ROT = {
    0: -90,
    1: 90,
    2: -180,
    3: 0,
}

CORE_CHILD_ORI = {0: (90, 0), 1: (-90, 0), 2: (0, 90), 3: (0, -90)}
"""dict: module level constants
Dictionaries that define the position and rotation of the children of the core component
"""

VIEW = 1
"""dict: module level variable
Variable that keeps track of the camera view
"""

CORE_COUNT = 0
HINGE_COUNT = 0
BRICK_COUNT = 0
"""dict: module level variable
Variables that keep track of quantity of different parts
"""

BRUSH = BRICK
ORI = 0
"""dict: module level variable
Variables that enable different creation modes
"""

# =============================== Ursina ===================================== #
class Voxel(Button):
    def __init__(self, parent, _type, position, orientation, idx):
        part_model, part_color = self.get_model_info(_type, orientation)
        super().__init__(
            parent=parent,
            position=position,
            model=f"{part_model}.obj",
            texture=f"{part_model}.jpg",
            color=part_color,
            highlight_color=color.lime,
        )
        self.idx = idx
        self._type = _type
        self.orientation = orientation
        self.color = part_color
        global CORE_COUNT, BRICK_COUNT, HINGE_COUNT
        if _type == CORE:
            CORE_COUNT += 1
        elif _type == BRICK:
            BRICK_COUNT += 1
        elif _type == HINGE:
            HINGE_COUNT += 1
        self.as_dict = self.get_as_dict()

    def get_model_info(self, _type, orientation):
        return ASSETS[_type], COLORS[orientation][_type]

    def get_type_count(self, _type):
        global CORE_COUNT, BRICK_COUNT, HINGE_COUNT
        if _type == CORE:
            return CORE_COUNT
        elif _type == BRICK:
            return BRICK_COUNT
        elif _type == HINGE:
            return HINGE_COUNT

    def get_as_dict(self):
        """
        Args:
            _id: Identifier of part, arbitrary
            _type: Type of component to return, categorical = {C, H, B}
            orientation: Rotation of component, categorical = {0, 90}
            b: Blue component of part color, range = [0-1]
            g: Green component of part color, range = [0-1]
            r: Red component of part color, range = [0-1]

        Returns: dictionary with correctly formatted keys for YAML file
        """
        # Generate Id
        _id = f"{self._type}{self.orientation}_{self.get_type_count(self._type)}"

        # Build Part
        part = {}
        part[ID] = _id
        part[TYPE] = self._type
        part[ORIENTATION] = self.orientation
        part[PARAMS] = {}
        part[PARAMS][RED] = self.color[0]
        part[PARAMS][GREEN] = self.color[1]
        part[PARAMS][BLUE] = self.color[2]
        return part

    def input(self, key):
        if self.hovered:
            if key == "left mouse down":
                if self._type == CORE:
                    idx = pos_2_dir(mouse.normal, core=True)
                    if idx == None:
                        pass
                    else:
                        voxel = Voxel(
                            parent=self,
                            _type=BRUSH,
                            position=mouse.normal,
                            orientation=ORI,
                            idx=idx,
                        )
                        voxel.rotation_z = CORE_CHILD_ROT[idx]
                        if ORI == 90:
                            voxel.rotation_x, voxel.rotation_y = CORE_CHILD_ORI[idx]
                else:
                    idx = pos_2_dir(mouse.normal)
                    if idx == None:
                        pass
                    else:
                        voxel = Voxel(
                            parent=self,
                            _type=BRUSH,
                            position=mouse.normal,
                            orientation=ORI,
                            idx=idx,
                        )
                        voxel.rotation_z = dir_2_rot(idx)
                        if ORI == 90:
                            voxel.rotation_x, voxel.rotation_y = dir_2_ori(idx)

            if key == "right mouse down" and self._type != CORE:
                destroy(self)


def pos_2_dir(pos, core: bool = False):
    if core:
        if pos == (-1, 0, 0):
            return 0
        elif pos == (1, 0, 0):
            return 1
        elif pos == (0, -1, 0):
            return 2
        elif pos == (0, 1, 0):
            return 3
        else:
            return None
    else:
        if pos == (-1, 0, 0):
            return 3
        elif pos == (1, 0, 0):
            return 2
        elif pos == (0, -1, 0):
            return 0
        elif pos == (0, 1, 0):
            return 1
        else:
            return None


def dir_2_pos(direction):
    if direction == 3:
        return (-1, 0, 0)
    elif direction == 2:
        return (1, 0, 0)
    elif direction == 0:
        return (0, -1, 0)
    elif direction == 1:
        return (0, 1, 0)
    else:
        return None


def dir_2_rot(direction):
    if direction == 0:
        return -180
    elif direction == 1:
        return
    elif direction == 2:
        return 90
    elif direction == 3:
        return -90
    else:
        return None


def dir_2_ori(direction):
    if direction == 1:
        return 0, -90
    elif direction == 2:
        return -90, 0
    elif direction == 3:
        return 90, 0
    else:
        return None


def recursive_draw_parts(data, voxel):
    try:
        keys = data[CHILDREN].keys()
    except KeyError:
        return
    for child_idx in keys:
        _type = data[CHILDREN][child_idx][TYPE]
        child = Voxel(
            parent=voxel,
            _type=_type,
            position=dir_2_pos(child_idx),
            orientation=data[CHILDREN][child_idx][ORIENTATION],
            idx=child_idx,
        )
        child.rotation_z = dir_2_rot(child_idx)
        if data[CHILDREN][child_idx][ORIENTATION] == 90:
            child.rotation_x, child.rotation_y = dir_2_ori(child_idx)

        try:
            recursive_draw_parts(data[CHILDREN][child_idx], child)
        except KeyError:
            pass


def yaml_2_scene(data: dict) -> None:
    """
    Adds YAML file contents to scene
    """
    # Draw core component
    core_data = data[BODY]
    _type = core_data[TYPE]
    global core

    for child_idx in core_data[CHILDREN].keys():
        _type = core_data[CHILDREN][child_idx][TYPE]
        child = Voxel(
            parent=core,
            _type=_type,
            position=CORE_CHILD_POS[child_idx],
            orientation=core_data[CHILDREN][child_idx][ORIENTATION],
            idx=child_idx,
        )
        child.rotation_z = CORE_CHILD_ROT[child_idx]
        if core_data[CHILDREN][child_idx][ORIENTATION] == 90:
            child.rotation_x, child.rotation_y = CORE_CHILD_ORI[child_idx]

        recursive_draw_parts(core_data[CHILDREN][child_idx], child)


def yaml_read(yaml_path: str) -> dict:
    """
    Args:
        yaml_in: name of YAML file to read

    Returns: A dictionary containing the contents of the YAML file
    """
    with open(yaml_path) as f:
        data = yaml.load(f, Loader=yaml.FullLoader)
    return data


def engine_setup() -> None:
    """ """
    # Window improvements
    window.title = "Devolve"  # The window title
    window.borderless = False  # Show a border
    window.fullscreen = False  # Do not go Fullscreen
    window.exit_button.visible = False  # Hide in-game red X that loses the window
    window.fps_counter.enabled = True  # Show the FPS (Frames per second) counter

    # Enable movable camera
    # Key-bindings:
    #   toggle_orthographic: [shift+p]
    #   focus: [f]
    #   reset_center: [shift+f]
    global ec
    ec = EditorCamera()


class MenuButton(Button):
    def __init__(self, text="", **kwargs):
        super().__init__(
            text, scale=(0.18, 0.05), highlight_color=color.light_gray, **kwargs
        )

        for key, value in kwargs.items():
            setattr(self, key, value)


def function_menu() -> None:
    """ """

    def yaml_construct_recusrive(voxel, data):
        children = voxel.children
        if len(children) > 0:
            data[CHILDREN] = {}
            for child in children:
                data[CHILDREN][child.idx] = child.as_dict
                data[CHILDREN][child.idx] = yaml_construct_recusrive(
                    child, data[CHILDREN][child.idx]
                )
        return data

    def save_yaml() -> None:
        """ """
        wp = FileBrowserSave(file_type=".yaml")

        global core
        data = yaml_construct_recusrive(core, core.as_dict)
        yaml_out = {ID: "robot", BODY: data}
        wp.data = yaml.dump(yaml_out, sort_keys=False)

    def load_yaml() -> None:
        """ """
        fb = FileBrowser(file_types=("*.yaml"), enabled=True)

        def on_submit(paths):
            sys.stdout.write("======= STARTING YAML LOADING =======\n")
            clear_canvas()
            for p in paths:
                sys.stdout.write(f"--- {p}\n")
                data = yaml_read(p)  # Get YAML data
                yaml_2_scene(data)  # Render YAMl data
            sys.stdout.write("======= ENDING YAML LOADING =======\n")
            sys.stdout.flush()

        fb.on_submit = on_submit

    def clear_canvas() -> None:
        """ """
        global core
        for child in core.children:
            destroy(child)

    def change_view() -> None:
        """ """
        global VIEW, ec
        if VIEW == 0:
            ec.position = (0, 0, 0)
            ec.rotation = (0, 0, 0)
            VIEW = 1
        elif VIEW == 1:
            ec.position = (-0.02, -0.33, -0.14)
            ec.rotation = (25, 25, 0)
            VIEW = 2
        elif VIEW == 2:
            ec.position = (0, -0.29, -0.053)
            ec.rotation = (0, -90, 0)
            VIEW = 3
        elif VIEW == 3:
            ec.position = (-0.11, -0.23, 0)
            ec.rotation = (90, 0, 0)
            VIEW = 0

    button_spacing = 0.05 * 1.25
    menu_parent = Entity(parent=camera.ui, y=0.40, x=-0.65)
    menu_parent.buttons = [
        MenuButton("Save YAML", on_click=save_yaml),
        MenuButton("Load YAML", on_click=load_yaml),
        MenuButton("Clear Canvas", on_click=clear_canvas),
        MenuButton("Change View", on_click=change_view),
    ]
    for i, e in enumerate(menu_parent.buttons):
        e.parent = menu_parent
        e.y = -i * button_spacing


def brush_menu() -> None:
    """ """

    def toggle_brush() -> None:
        """ """
        global BRUSH
        if BRUSH == BRICK:
            BRUSH = HINGE
            menu_parent.buttons[0].text = "Hinge"
        else:
            BRUSH = BRICK
            menu_parent.buttons[0].text = "Brick"
        menu_parent.buttons[0].color = COLORS[ORI][BRUSH]

    def toggle_rotation() -> None:
        global ORI
        if ORI == 0:
            ORI = 90
            menu_parent.buttons[1].text = "Rotated"
        else:
            ORI = 0
            menu_parent.buttons[1].text = "Normal"
        menu_parent.buttons[0].color = COLORS[ORI][BRUSH]

    button_spacing = 0.18 * 1.15
    menu_parent = Entity(parent=camera.ui, y=-0.45, x=0.11)
    menu_parent.buttons = [
        MenuButton("Bricks", on_click=toggle_brush, color=COLORS[ORI][BRUSH]),
        MenuButton("Normal", on_click=toggle_rotation),
    ]
    for i, e in enumerate(menu_parent.buttons):
        e.parent = menu_parent
        e.x = -i * button_spacing


def main() -> None:
    """ """
    # TODO
    function_menu()

    # TODO
    brush_menu()

    # Initialize world with "core" component
    global core
    core = Voxel(parent=scene, _type=CORE, position=(0, 0, 0), orientation=0, idx=None)


if __name__ == "__main__":
    # Initialise your Ursina app
    app = Ursina()

    # Set up engine parameters
    engine_setup()

    # Enter main loop of application
    main()

    # Run the app
    app.run()
