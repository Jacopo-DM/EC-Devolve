#!/usr/bin/env python3
from math import radians, degrees
from os import chdir
from ursina import collider, texture
import yaml as pyyaml
import numpy as np
from math import cos, sin, radians, degrees
from copy import deepcopy
from ursina import *
import sys

# Global Params Parser
HINGE_COUNT = 0
BRICK_COUNT = 0
# Global Params Ursina
SIZE = 20
HALF_SIZE = int(SIZE/2)
X_CENTER = int(SIZE/2)
Y_CENTER = int(SIZE/2)
CUBE_UNIT = 0.1
PART_COLORS = {'CoreComponent': {0: 'FFFFFF', 90: 'FFFFFF'},
               'FixedBrick': {0: '1F47FF', 90: 'FFB400'},
               'ActiveHinge': {0: '94FF00', 90: 'FF0070'}
               }
MODELS = {'CoreComponent': 'models/core/core.obj',
          'FixedBrick': 'models/brick/brick.obj',
          'ActiveHinge': 'models/hinge/hinge.obj'
          }

TEXTURES = {'CoreComponent': 'models/core/core_na.png',
            'FixedBrick': 'models/brick/brick_na.png',
            'ActiveHinge': 'models/hinge/hinge_na.png'
            }


####################################### LOGISTICS #######################################


def angle_between(v1, v2):
    return degrees(np.arccos(np.clip(np.dot(v1, v2), -1.0, 1.0)))


def Rx(theta: int) -> np.array:
    return np.array([[1, 0, 0],
                     [0, np.cos(theta), -np.sin(theta)],
                     [0, np.sin(theta), np.cos(theta)]]).astype(int)


def Ry(theta: int) -> np.array:
    return np.array([[np.cos(theta), 0, np.sin(theta)],
                     [0, 1, 0],
                     [-np.sin(theta), 0, np.cos(theta)]]).astype(int)


def Rz(theta: int) -> np.array:
    return np.array([[np.cos(theta), -np.sin(theta), 0],
                     [np.sin(theta), np.cos(theta), 0],
                     [0, 0, 1]]).astype(int)


def rotation_matrix_from_vectors(vec1, vec2):
    a, b = (vec1 / np.linalg.norm(vec1)).reshape(3), (vec2 /
                                                      np.linalg.norm(vec2)).reshape(3)
    v = np.cross(a, b)
    c = np.dot(a, b)
    s = np.linalg.norm(v)
    kmat = np.array([[0, -v[2], v[1]], [v[2], 0, -v[0]], [-v[1], v[0], 0]])
    rotation_matrix = np.eye(3) + kmat + kmat.dot(kmat) * ((1 - c) / (s ** 2))
    return rotation_matrix


def get_cardinal_vectors(compass: np.array, child_idx: int) -> list:
    # Y-Axis
    zero = np.negative(compass[1, :]).squeeze().astype(int)
    one = compass[1, :].squeeze().astype(int)

    # X-Axis
    two = compass[0, :].squeeze().astype(int)
    three = np.negative(compass[0, :]).squeeze().astype(int)

    # Z-Axis
    up = compass[2, :].flatten()
    down = np.negative(compass[2, :].flatten())

    # Return Directions
    if child_idx == 0:
        return [one, zero]
    elif child_idx == 1:
        return [one, one]
    elif child_idx == 2:
        return [one, two]
    elif child_idx == 3:
        return [one, three]
    elif child_idx == -1:
        return [zero, one, two, three, up, down]


def rotate_90(compass: np.array):
    return compass.dot(Ry(radians(90)))


def rotate_90_neg(compass: np.array):
    return compass.dot(Ry(radians(-90)))


class Module:
    ID = 'id'
    BODY = 'body'
    TYPE = 'type'
    ORIENTATION = 'orientation'
    PARAMS = 'params'
    B = 'blue'
    G = 'green'
    R = 'red'
    HINGE = 'ActiveHinge'
    BRICK = 'FixedBrick'
    CORE = 'CoreComponent'
    PART_TYPES = [HINGE, BRICK, CORE]
    PART_ORIENTATIONS = [0, 90]
    RGB_RANGE = [0, 1]
    CHILDREN = 'children'
    DIRECTIONS = [0, 1, 2, 3]


    # Accepted Colors
    # FFFFFF
    COLOR_C = {B: 1, G: 1, R: 1}            # Core
    # 1F47FF
    COLOR_BN = {R: .122, G: .278, B: 1}     # Brick Normal Orientation
    # FFB400
    COLOR_BR = {R: 1, G: .706, B: 0}        # Brick @ 90 Degrees
    # 94FF00
    COLOR_HN = {R: 1, G: 0, B: .439}        # Hinge Normal Orientation
    # FF0070
    COLOR_HR = {R: .58, G: 1, B: 0}          # Hinge @ 90 Degrees
    ACCEPTED_COLORS = [COLOR_C, COLOR_BN, COLOR_BR, COLOR_HN, COLOR_HR]

PART_COLORS = {'CoreComponent': {0: 'FFFFFF', 90: 'FFFFFF'},
               'FixedBrick': {0: '1F47FF', 90: 'FFB400'},
               'ActiveHinge': {0: '94FF00', 90: 'FF0070'}
               }

class Grid(Module):
    # ======== INIT ======== #
    def __init__(self, x: int, y: int, z: int) -> None:
        # Grid Dimensions
        self.dim_x = x
        self.dim_y = y
        self.dim_z = z

        # Grid Elements
        self.elements_init()
        self.grid = np.zeros([self.dim_x, self.dim_y, self.dim_z])

# ======== FUNCTIONS ======== #
    def get_view(self, depth: int = -1) -> np.array:
        if self.size[2] == 1:
            view = self.grid.reshape((self.dim_x, self.dim_y))
        else:
            if depth == -1:
                depth = int(self.dim_z/2)+1
            sys.stdout.write(
                f"CAREFUL! THERE ARE MULTIPLE Z-LEVELS ({self.dim_z}), SEEING {depth} \n")
            view = self.grid[:, :, depth-1].reshape((self.dim_x, self.dim_y))
        return view

    def elements_init(self) -> None:
        self.elements = {}
        for x in range(0, self.dim_x):
            self.elements[x] = {}
            for y in range(0, self.dim_y):
                self.elements[x][y] = {}
                for z in range(0, self.dim_z):
                    self.elements[x][y][z] = {0: None}

    def grid_init(self) -> None:
        self.grid = np.zeros((self.dim_x, self.dim_y, self.dim_z))

    def insert_element(self, x: int, y: int, z: int, entry, compass: np.array) -> None:
        if 0 in self.elements[x][y][z]:
            self.elements[x][y][z] = {1: entry, 'compass': compass}
            self.grid[x][y][z] = 1
        else:
            try:
                raise ValueError(
                    'Over-writing grid-entry!')
            except Exception as error:
                sys.stdout.write('Caught other error: ' + repr(error) + '\n')
                raise

    def remove_element(self, x: int, y: int, z: int) -> None:
        self.elements[x][y][z] = {0: None}
        self.grid[x][y][z] = 0

# ======== PROPERTIES ======== #
    @property
    def size(self) -> list:
        return [self.dim_x, self.dim_y, self.dim_z]

    @property
    def dim_x(self) -> int:
        return self._dim_x

    @property
    def dim_y(self) -> int:
        return self._dim_y

    @property
    def dim_z(self) -> int:
        return self._dim_z

    @dim_x.setter
    def dim_x(self, x: int) -> None:
        self.check_dim(x)
        self._dim_x = x

    @dim_y.setter
    def dim_y(self, y: int) -> None:
        self.check_dim(y)
        self._dim_y = y

    @dim_z.setter
    def dim_z(self, z: int) -> None:
        self.check_dim(z)
        self._dim_z = z

# ======== CHECKS ======== #
    def check_dim(self, dim: int) -> None:
        if dim <= 0:
            try:
                raise ValueError(
                    'Dimension Can\'t Be Negative or Zero! : {ARG}')
            except Exception as error:
                sys.stdout.write('Caught other error: ' + repr(error) + '\n')
                raise


class Component(Module):
    # ======== INIT ======== #
    def __init__(self, id_: str, x: int, y: int, z: int) -> None:
        # Global Counters
        global HINGE_COUNT, BRICK_COUNT

        # Functional
        self.yaml = {}
        self.ready_2_output = False
        self._x = x   # TODO: make property, check if right
        self._y = y   # TODO: make property, check if right
        self._z = z   # TODO: make property, check if right

        # YAML parts
        if id_ == 'core':
            self.id_ = id_.capitalize()
            self.make_core()
        elif id_ == 'hinge0_':
            self.id_ = f'{id_}{HINGE_COUNT}'.capitalize()
            self.make_hinge()
            HINGE_COUNT += 1
        elif id_ == 'hinge90_':
            self.id_ = f'{id_}{HINGE_COUNT}'.capitalize()
            self.make_hinge_90()
            HINGE_COUNT += 1
        elif id_ == 'brick0_':
            self.id_ = f'{id_}{BRICK_COUNT}'.capitalize()
            self.make_brick()
            BRICK_COUNT += 1
        elif id_ == 'brick90_':
            self.id_ = f'{id_}{BRICK_COUNT}'.capitalize()
            self.make_brick_90()
            BRICK_COUNT += 1
        else:
            try:
                raise ValueError(f'Unknown Identifier Arguemnt (id_): {id_}')
            except Exception as error:
                sys.stdout.write('Caught other error: ' + repr(error) + '\n')
                raise

# ======== FUNCTIONS ======== #
    def make_yaml(self) -> None:
        if self._ready_2_output:
            self.yaml[self.ID] = self.id_
            self.yaml[self.TYPE] = self.type_
            self.yaml[self.ORIENTATION] = self.orientation
            self.yaml[self.PARAMS] = self.params
            for child in self.children:
                if self.children[child] != None:
                    if self.CHILDREN not in self.yaml:
                        self.yaml[self.CHILDREN] = {}
                    self.children[child].make_yaml()
                    self.yaml[self.CHILDREN][child] = self.children[child].yaml
        else:
            try:
                raise ValueError(
                    'Can\'t Output YAML: Component Is Missing Definitions')
            except Exception as error:
                sys.stdout.write('Caught other error: ' + repr(error) + '\n')
                raise

    def make_core(self) -> None:
        self.make_part(self.CORE, 0, **self.COLOR_C)

    def make_hinge(self) -> None:
        self.make_part(self.HINGE, 0, **self.COLOR_HN)

    def make_hinge_90(self) -> None:
        self.make_part(self.HINGE, 90, **self.COLOR_HR)

    def make_brick(self) -> None:
        self.make_part(self.BRICK, 0, **self.COLOR_BN)

    def make_brick_90(self) -> None:
        self.make_part(self.BRICK, 90, **self.COLOR_BR)

    def make_part(self, type_: str, orientation: int, blue: int, green: int, red: int) -> None:
        self.type_ = type_
        self.orientation = orientation
        self.params = [blue, green, red]
        self.children = {0: None, 1: None, 2: None, 3: None}
        self.ready_2_output = True

    def set_child(self, direction: int, child: object) -> None:
        self.check_child(direction, child)
        self.children[direction] = child


# ======== PROPERTIES ======== #
    # Getters


    @property
    def x(self) -> int:
        return self._x

    @property
    def y(self) -> int:
        return self._y

    @property
    def z(self) -> int:
        return self._z

    @property
    def id_(self) -> str:
        return self._id_

    @property
    def type_(self) -> str:
        return self._type_

    @property
    def orientation(self) -> int:
        return self._orientation

    @property
    def params(self) -> set:
        return self._params

    @property
    def ready_2_output(self) -> bool:
        return self._ready_2_output

    # Setters
    @id_.setter
    def id_(self, id_: str):
        self._id_ = id_

    @type_.setter
    def type_(self, type_: str):
        self.check_type(type_)
        self._type_ = type_

    @orientation.setter
    def orientation(self, orientation: int):
        self._orientation = orientation

    @params.setter
    def params(self, colors: list):
        self.check_params(colors[0], colors[1], colors[2])
        self._params = {self.B: colors[0],
                        self.G: colors[1], self.R: colors[2]}

    @ready_2_output.setter
    def ready_2_output(self, r2p: bool):
        self._ready_2_output = r2p

# ======== CHECKS ======== #
    def check_type(self, _type: str) -> None:
        if _type not in self.PART_TYPES:
            try:
                raise ValueError(f'Problem with _type argument: {_type}')
            except Exception as error:
                sys.stdout.write('Caught other error: ' + repr(error) + '\n')
                raise

    def check_orientation(self, orientation: int) -> None:
        if orientation not in self.PART_ORIENTATIONS:
            try:
                raise ValueError(
                    f'Problem with orientation argument: {orientation}')
            except Exception as error:
                sys.stdout.write('Caught other error: ' + repr(error) + '\n')
                raise

    def check_params(self, blue: float, green: float, red: float) -> None:
        bgr_min = self.RGB_RANGE[0]
        bgr_max = self.RGB_RANGE[1]
        for color in [blue, green, red]:
            if color < bgr_min or color > bgr_max:
                try:
                    raise ValueError(
                        f'Color value out of range: [{blue},{green},{red}]')
                except Exception as error:
                    sys.stdout.write(
                        'Caught other error: ' + repr(error) + '\n')
                    raise

        temp_params = {self.B: blue, self.G: green, self.R: red}
        if temp_params not in self.ACCEPTED_COLORS:
            try:
                raise ValueError(
                    f'Problem with params argument: {temp_params}')
            except Exception as error:
                sys.stdout.write('Caught other error: ' + repr(error) + '\n')
                raise

    def check_child(self, direction: int, child: object) -> None:
        if direction not in self.DIRECTIONS:
            try:
                raise ValueError(
                    f'Non-existant direction of child: {direction}')
            except Exception as error:
                sys.stdout.write('Caught other error: ' + repr(error) + '\n')
                raise
        if isinstance(child, Component) != True:
            try:
                raise ValueError(
                    f'Child must be of class "Component", current is: {type(child)}')
            except Exception as error:
                sys.stdout.write('Caught other error: ' + repr(error) + '\n')
                raise


class Parser(Module):
    def yaml_parser(self, yaml: set, component: Component, compass: np.array, grid: Grid) -> None:
        for child_index in yaml:
            type_ = yaml[child_index][self.TYPE]
            orientation = yaml[child_index][self.ORIENTATION]
            conversion = {
                self.HINGE: 'hinge',
                self.BRICK: 'brick'
            }
            # Form partial id of part
            id_ = f'{conversion[type_]}{orientation}_'

            # Return direction of child
            new_compass = deepcopy(compass)
            start_vec, end_vec = get_cardinal_vectors(new_compass, child_index)
            if child_index != 1:
                if child_index == 0:
                    __, temp_vec = get_cardinal_vectors(new_compass, 2)
                    start_2_temp = rotation_matrix_from_vectors(
                        end_vec, temp_vec)
                    new_compass = new_compass.dot(start_2_temp)
                    new_compass = new_compass.dot(start_2_temp)
                else:
                    start_2_end = rotation_matrix_from_vectors(
                        end_vec, start_vec)
                    new_compass = new_compass.dot(start_2_end)

            # Rotate part by orientation orientation
            if orientation == 90:
                new_compass = rotate_90(new_compass)

            # Get New Direction
            new_x = component.x + int(end_vec[1])
            new_y = component.y + int(end_vec[0])
            new_z = component.z + int(end_vec[2])

            new_component = Component(id_, new_x, new_y, new_z)
            component.set_child(child_index, new_component)
            grid.insert_element(new_component.x, new_component.y,
                                new_component.z, new_component, deepcopy(new_compass))

            # Intermediate 2D Array View
            # view = grid.get_view()
            # print(view)

            # Catch Leafs
            if self.CHILDREN in yaml[child_index]:
                new_yaml = yaml[child_index][self.CHILDREN]
                self.yaml_parser(new_yaml, new_component, new_compass, grid)

            # Undo rotations
            if child_index != 1:
                end_2_start = rotation_matrix_from_vectors(start_vec, end_vec)
                new_compass = new_compass.dot(end_2_start)

            if orientation == 90:
                new_compass = rotate_90_neg(new_compass)

####################################### URSINA #######################################


class Inventory(Entity):
    def __init__(self):
        super().__init__(
            parent=camera.ui,
            scale=(CUBE_UNIT, CUBE_UNIT*4),
            origin=(0, 0),
            texture='white_cube',
            position=(-CUBE_UNIT*7, 0),
            texture_scale=(1, 4),
            color=color.white
        )
        self.item_parent = Entity(parent=self, scale=(1, 1/4))


class Voxel(Entity):
    def __init__(self, position=(0, 0, 0)):
        super().__init__(
            parent=scene,
            position=position,
            origin_y=.5,
            collider=None,
        )
        print(self.position.x, self.position.y, self.position.z)
        self.button = Button(parent=self, model='cube', texture='cube',
                             color=color.white10, highlight_color=color.orange, position=(0,0,0), collider='box')

    def input(self, key):
        if self.button.hovered:
            if key == 'left mouse down':
                voxel = Voxel(position=self.button.position + mouse.normal)
            if key == 'right mouse down':
                destroy(self)


class Editor(Entity):
    def __init__(self, elements, **kwargs):
        super().__init__()

        # Make Inventory
        self.inventory = Inventory()
        btn_hinge0 = self.make_icon(
            'Up/Down Hinge', (0, 1), PART_COLORS['ActiveHinge'][0])
        btn_hinge90 = self.make_icon(
            'Left/Right Hinge', (0, 0), PART_COLORS['ActiveHinge'][90])
        btn_brick0 = self.make_icon(
            'Brick Normal', (0, -1), PART_COLORS['FixedBrick'][0])
        btn_brick90 = self.make_icon(
            'Brick Rotated', (0, -2), PART_COLORS['FixedBrick'][90])

        # # Add button function
        # up_down.on_click = self.change_cursor_red
        # left_right.on_click = self.change_cursor_green
        # structural.on_click = self.change_cursor_blue

    def make_icon(self, item, pos, clr):
        icon = Button(
            parent=self.inventory.item_parent,
            scale=(.9, .9),
            model='quad',
            origin=(0, 0),
            position=pos,
            texture='white_cube',
            highlight_color=color.white,
            color=clr,
            z=-.1,
        )
        name = item.replace('_', ' ').title()
        icon.tooltip = Tooltip(name)
        return icon

    # def change_cursor_red(self):
    #     self.cursor.color = color.red

    # def change_cursor_green(self):
    #     self.cursor.color = color.green

    # def change_cursor_blue(self):
    #     self.cursor.color = color.blue

####################################### MAIN CALL #######################################


def main(yaml_file):
    ## WORK WITH DATA ##
    body = yaml_file['body']
    current = body['children']

    # Parameters
    x_center, y_center, z_center = HALF_SIZE, HALF_SIZE, HALF_SIZE

    # Object
    core = Component('core', x=x_center, y=y_center, z=z_center)

    grid = Grid(SIZE, SIZE, SIZE)
    parser = Parser()
    compass = np.eye(3)

    # Initilize Grid
    grid.insert_element(core.x, core.y, core.z, core, deepcopy(compass))

    # Parse YAML
    parser.yaml_parser(current, core, compass, grid)
    # view = grid.get_view()
    # print(view)

    # Get YAML
    core.make_yaml()
    yaml_file = core.yaml

    # Get Grid
    elements = grid.elements

    # Render Loop
    for x in range(0, SIZE):
        for y in range(0, SIZE):
            for z in range(0, SIZE):
                temp = elements[x][y][z]
                if 1 in temp:
                    voxel = Voxel((
                        x-HALF_SIZE, y-HALF_SIZE, z-HALF_SIZE))

                    # voxel.position =
                    voxel.color = color.hex(
                        PART_COLORS[temp[1].type_][temp[1].orientation])
                    voxel.model = MODELS[temp[1].type_]
                    voxel.texture = TEXTURES[temp[1].type_]
                    if temp[1].id_ == 'Core':
                        continue
                    rotation = temp['compass'][1] * -90
                    voxel.rotation = [rotation[1],
                                      rotation[2], rotation[0]]

    editor = Editor(elements)
    return yaml_file


if __name__ == '__main__':
    # Start Ursina
    app = Ursina()

    ####################

    # Read Input From YAML File
    # path = './test.yaml'
    path = './tardigrade.yaml'
    # path = './phenotypes/phenotype_1.yaml'
    # path = './phenotypes/phenotype_10.yaml' # Overwrite
    # path = './phenotypes/phenotype_100.yaml'
    # path = './phenotypes/phenotype_228.yaml'
    with open(path) as f:
        data = pyyaml.load(f, Loader=pyyaml.FullLoader)

    # Main Loop
    data = main(data)

    # Add Header
    top = {}
    top['id'] = 'out'
    top['body'] = {}
    top['body'] = data
    data = top

    # Write Output To YAML File
    name = 'out'
    path = ('./' + name + '.yaml')
    with open(path, 'w') as f:
        pyyaml.dump(data, f, sort_keys=False)

    ####################

    # hotkeys = {'toggle_orthographic':'shift+p', 'focus':'f', 'reset_center':'shift+f'}
    EditorCamera()
    app.run()
