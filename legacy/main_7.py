""" Code Info
Author:     Jacopo Di Matteo
Date:       27.01.2022

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

- [ ]: Integrate automatic installation of packages?
- [ ]: Ursina import only necessary

This code is provided 'As Is'.
"""

# Imports (3rd Party)
import yaml
from ursina import *

# Global Constants (Needed For Intellisense And Extendability)
ID = "id"
BODY = "body"
TYPE = "type"
ORIENTATION = "orientation"
PARAMS = "params"
BLUE = "blue"
GREEN = "green"
RED = "red"
CHILDREN = "children"
CORE = "CoreComponent"
HINGE = "ActiveHinge"
BRICK = "FixedBrick"
"""string: module level constants, YAML headers definitions
Needed for future proof, as the naming choice for Revolve is arbitrary
"""

PARTS = {
    "C": CORE,
    "H": HINGE,
    "B": BRICK,
}
""" dict: module level constant, for convenience
Dictionary that has as abbreviations of parts as keys, linked to the full name of parts
"""

core_count = 0  # This is only for future-proofing, as there can only be 1 core
hinge_count = 0
brick_count = 0
""" int: module level variable
Two variables to keep count of different parts
"""

COLOR_C0 = {"b": 1, "g": 1, "r": 1}  # White
COLOR_H0 = {"b": 1, "g": 0, "r": 0.439}  # TODO: Color name
COLOR_H90 = {"b": 0.58, "g": 1, "r": 0}  # TODO: Color name
COLOR_B0 = {"b": 0.122, "g": 0.278, "r": 1}  # TODO: Color name
COLOR_B90 = {"b": 1, "g": 0.706, "r": 0}  # TODO: Color name
""" dict: module level constants
Colors needed to color robot parts, as dictionaries
"""

MODELS = {
    "CoreComponent": "models/core/core.obj",
    "FixedBrick": "models/brick/brick.obj",
    "ActiveHinge": "models/hinge/hinge.obj",
}
TEXTURES = {
    "CoreComponent": "models/core/core_na.png",
    "FixedBrick": "models/brick/brick_na.png",
    "ActiveHinge": "models/hinge/hinge_na.png",
}
"""dict: module level constants
Dictionaries that define path to model asssets
"""


def update_type_count(_type: str) -> None:
    """
    Updates the global variables which keep count of the number of parts.
    Used for 'id' generation, for the 'id' tag in the YAML file

    Args:
        _type: Specifies which part-counter to increase
    """
    if _type == "H":
        global hinge_count
        hinge_count += 1
    elif _type == "B":
        global brick_count
        brick_count += 1
    elif _type == "C":  # This is only for future-proofinf, as there can only be 1 core
        global core_count
        core_count += 1
    else:
        raise ValueError(f"Illegal '_type' argument: {_type}")


def get_type_count(_type: str) -> int:
    """
    Cleanly returns the global variable which holds the counts of parts

    Args:
        _type: Specifies which part-counter to return

    Returns: returns the count of a given part
    """
    if _type == "H":
        global hinge_count
        return hinge_count
    elif _type == "B":
        global brick_count
        return brick_count
    elif _type == "C":
        global core_count
        return core_count
    else:
        raise ValueError(f"Illegal '_type' argument: {_type}")


def get_part_as_dict(_type: str, orientation: int, b: int, g: int, r: int) -> dict:
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
    _id = f"{_type}{orientation}_{get_type_count(_type)}"

    # Update counter
    update_type_count(_type)

    # Build Part
    part = {}
    part[ID] = _id
    part[TYPE] = PARTS[_type]
    part[ORIENTATION] = orientation
    part[PARAMS] = {}
    part[PARAMS][BLUE] = b
    part[PARAMS][GREEN] = g
    part[PARAMS][RED] = r
    return part


def get_yaml_header(_id: str) -> dict:
    """
    Args:
        id: Identifier at the top of the YAML file

    Returns: returns a dictionary with the header information for the YAML file
    """
    return {ID: _id, BODY: get_part_as_dict("Core", "C", 0, **COLOR_C0)}


def get_hinge(orientation: int) -> dict:
    """
    Args:
        orientation: Specifies the orientation of the hinge, categorical = {0, 90}
    """
    # Check for orientation
    if orientation == 0:
        return get_part_as_dict("H", orientation, **COLOR_H0)
    elif orientation == 90:
        return get_part_as_dict("H", orientation, **COLOR_H90)
    else:
        raise ValueError(f"Illegal 'orientation' argument: {orientation}")


def get_brick(orientation: int) -> dict:
    """
    Args:
        orientation: Specifies the orientation of the brick, categorical = {0, 90}
    """
    # Check for orientation
    if orientation == 0:
        return get_part_as_dict("H", orientation, **COLOR_B0)
    elif orientation == 90:
        return get_part_as_dict("H", orientation, **COLOR_B90)
    else:
        raise ValueError(f"Illegal 'orientation' argument: {orientation}")


def yaml_print(yaml_out: dict) -> None:
    """
    Writes dictionary to ./[name].yaml
    Args:
        yaml: A dictionary which needs to be written to a YAML file
    """
    name = "tst"
    path = "./" + name + ".yaml"
    with open(path, "w") as f:
        yaml.dump(
            yaml_out, f, sort_keys=False
        )  # sort_keys=False to avoid re-arrangement


def yaml_read(yaml_in: str) -> dict:
    """
    Args:
        yaml_in: name of YAML file to read

    Returns: A dictionary containing the contents of the YAML file
    """
    path = f"./{yaml_in}.yaml"
    with open(path) as f:
        data = yaml.load(f, Loader=yaml.FullLoader)
    return data


class Voxel(Button):
    """
    TODO: See class docstring_template
    """

    def __init__(self, position: tuple = (0, 0, 0), clr: Color = color.white10) -> None:
        """
        TODO: Explain
        Args:
            position (int, int, int): (x, y, z) position of voxel
            clr: The color of voxel, Color(float, float, float, float), range = [0, 1]
        """
        super().__init__(
            parent=scene,
            model="cube",
            texture="white_cube",
            color=clr,
            # color=color.white10
            highlight_color=color.lime,
            scale=(1, 1, 1),
            position=position,
        )

    def input(self, key: str) -> None:
        """
        Reads keys from peripherals are performs actions in-game
        Args:
            key: a string holding the key being pressed
        """
        if self.hovered:
            pass


def child_idx_2_direction(child_idx: int, entity: Entity) -> LVector3f:
    """
    Returns the direction in which children of a part should be located

    Args:
        child_idx: child index as defined in YAML file, categorical = {0, 1, 2, 3}
        entity: parent entity to which the child is being added, ursina object

    Retruns: direction in which the child should be added
    """
    if child_idx == 0:  # This should NEVER happen, as it means going back to root
        return (round(entity.down.x), round(entity.down.y), round(entity.down.z))
    elif child_idx == 1:
        return (round(entity.up.x), round(entity.up.y), round(entity.up.z))
    elif child_idx == 2:
        return (round(entity.right.x), round(entity.right.y), round(entity.right.z))
    elif child_idx == 3:
        return (round(entity.left.x), round(entity.left.y), round(entity.left.z))
    else:
        raise ValueError(f"Illegal 'child_idx' argument: {child_idx}")


def engine_setup() -> None:
    """
    TODO: Explain
    """
    window.title = "Devolve"  # The window title
    window.borderless = False  # Show a border
    window.fullscreen = False  # Do not go Fullscreen
    window.exit_button.visible = False  # Hide in-game red X that loses the window
    window.fps_counter.enabled = True  # Show the FPS (Frames per second) counter
    EditorCamera()  # Enable movable


def recursive_draw_parts(
    part: dict, parent: Voxel, dir_x: int, dir_y: int, dir_z: int
) -> None:
    """
    TODO: Explain
    """
    colors = part[PARAMS]
    color = Color(colors[BLUE], colors[GREEN], colors[RED], 1.0)
    part_voxel = Voxel((dir_x, dir_y, dir_z), color)
    part_voxel.parent = parent
    part_voxel.model = MODELS[part[TYPE]]
    part_voxel.texture = TEXTURES[part[TYPE]]
    part_voxel.rotation_y += part[ORIENTATION]

    try:
        for child_idx in part[CHILDREN].keys():
            dir_x, dir_y, dir_z = child_idx_2_direction(child_idx, part_voxel)
            recursive_draw_parts(part[CHILDREN][child_idx], part_voxel, dir_x, dir_y, dir_z)
    except KeyError:  # Expect end of file (no children)
        children = {}

def yaml_2_scene(data: dict) -> None:
    """
    Adds YAML file contents to scene
    """
    print()
    print()
    print()

    # Draw core component
    core = data[BODY]
    colors = core[PARAMS]
    color = Color(colors[BLUE], colors[GREEN], colors[RED], 1.0)
    core_voxel = Voxel((0, 0, 0), color)
    core_voxel.model = MODELS[core[TYPE]]
    core_voxel.texture = TEXTURES[core[TYPE]]
    for child_idx in core[CHILDREN].keys():
        dir_x, dir_y, dir_z = child_idx_2_direction(child_idx, core_voxel)
        recursive_draw_parts(core[CHILDREN][child_idx], core_voxel, dir_x, dir_y, dir_z)

    print()
    print()
    print()


def scene_2_yaml() -> None:
    """
    Transforms a scene into a valid YAML file
    """
    pass


def main() -> None:

    # tst = get_yaml_header('out')
    # print(tst)

    # yaml_write(tst)

    # t1 = get_brick(0)
    # t2 = get_brick(90)
    # t3 = get_hinge(0)
    # t4 = get_hinge(90)
    # print(t1, t2, t3, t4)

    file_name = "out"
    file_name = "test"
    file_name = "tardigrade"
    file_name = "t2"
    # file_name = "phenotypes/phenotype_1"
    # file_name = "phenotypes/phenotype_10"
    # file_name = "phenotypes/phenotype_100"
    # file_name = 'phenotypes/phenotype_228' # TODO: Broken
    # data = yaml_read(file_name)
    # print(data)

    # voxel = Voxel()
    # print(voxel.forward)
    # c2 = Entity(model='cube', color=color.blue, scale=(1,1,1), texture = 'white_cube')

    data = yaml_read(file_name)
    yaml_2_scene(data)
    return


if __name__ == "__main__":
    app = Ursina()  # Initialise your Ursina app
    engine_setup()
    main()
    app.run()  # Run the app
