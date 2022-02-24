#!/usr/bin/env python3
from os import chdir
from ursina import texture
import yaml as pyyaml
import numpy as np
from math import cos, sin, radians, degrees
from copy import deepcopy
from ursina import *
import sys

HINGE_COUNT = 0
BRICK_COUNT = 0



def unit_vector(vector):
    return vector / np.linalg.norm(vector)

def angle_between(v1, v2):
    v1_u = unit_vector(v1)
    v2_u = unit_vector(v2)
    return degrees(np.arccos(np.clip(np.dot(v1_u, v2_u), -1.0, 1.0)))

def rotate_x(x: int, y: int, z: int, theta: int) -> list:
    # around the X-axis would be
    # |1     0           0| |x|   |        x        |   |x'|
    # |0   cos θ    −sin θ| |y| = |y cos θ − z sin θ| = |y'|
    # |0   sin θ     cos θ| |z|   |y sin θ + z cos θ|   |z'|
    rads = radians(theta)
    new_x = x
    new_y = y * cos(rads) - z * sin(rads)
    new_z = y * sin(rads) + z * cos(rads)
    return [int(new_x), int(new_y), int(new_z)]


def rotate_y(x: int, y: int, z: int, theta: int) -> list:
    # around the Y-axis would be
    # | cos θ    0   sin θ| |x|   | x cos θ + z sin θ|   |x'|
    # |   0      1       0| |y| = |         y        | = |y'|
    # |−sin θ    0   cos θ| |z|   |−x sin θ + z cos θ|   |z'|
    rads = radians(theta)
    new_x = x * cos(rads) + z * sin(rads)
    new_y = y
    new_z = -x * sin(rads) + z * cos(rads)
    return [int(new_x), int(new_y), int(new_z)]


def rotate_z(x: int, y: int, z: int, theta: int) -> list:
    # around the Z-axis would be
    # |cos θ   −sin θ   0| |x|   |x cos θ − y sin θ|   |x'|
    # |sin θ    cos θ   0| |y| = |x sin θ + y cos θ| = |y'|
    # |  0       0      1| |z|   |        z        |   |z'|
    rads = radians(theta)
    new_x = x * cos(rads) - y * sin(rads)
    new_y = x * sin(rads) - y * cos(rads)
    new_z = z
    return [int(new_x), int(new_y), int(new_z)]


class Compass:
    def __init__(self) -> None:
        self.compass = {
            0: [-1, 0, 0],
            1: [1, 0, 0],
            2: [0, 1, 0],
            3: [0, -1, 0],
        }

    def rotate(self, mode, theta) -> None:
        for direction in self.compass:
            x = self.compass[direction][0]
            y = self.compass[direction][1]
            z = self.compass[direction][2]
            if mode == 'x':
                new_x, new_y, new_z = rotate_x(x, y, z, theta)
            elif mode == 'y':
                new_x, new_y, new_z = rotate_y(x, y, z, theta)
            elif mode == 'z':
                new_x, new_y, new_z = rotate_z(x, y, z, theta)
            self.compass[direction][0] = new_x
            self.compass[direction][1] = new_y
            self.compass[direction][2] = new_z


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
    COLOR_C = {B: 1, G: 1, R: 1}            # Core
    # 1F47FF
    COLOR_BN = {B: .122, G: .278, R: 1}     # Brick Normal Orientation
    # FFB400
    COLOR_BR = {B: 1, G: .706, R: 0}        # Brick @ 90 Degrees
    # 94FF00
    COLOR_HN = {B: 1, G: 0, R: .439}        # Hinge Normal Orientation
    # FF0070
    COLOR_HR = {B: .58, G: 1, R: 0}          # Hinge @ 90 Degrees
    ACCEPTED_COLORS = [COLOR_C, COLOR_BN, COLOR_BR, COLOR_HN, COLOR_HR]


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
                f"CAREFUL! THERE ARE MULTIPLE Z-LEVELS ({self.dim_z}), SEEING {depth}")
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

    def insert_element(self, x: int, y: int, z: int, entry, compass: Compass) -> None:
        if 0 in self.elements[x][y][z]:
            self.elements[x][y][z] = {1: entry, 'compass': compass}
            self.grid[x][y][z] = 1
        else:
            try:
                raise ValueError(
                    'Over-writing grid-entry!')
            except Exception as error:
                sys.stdout.write('Caught other error: ' + repr(error))
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
                sys.stdout.write('Caught other error: ' + repr(error))
                raise


class Component(Module):
    # ======== INIT ======== #
    def __init__(self, id_: str, x: int, y: int, z: int) -> None:
        # Global Counters
        global HINGE_COUNT, BRICK_COUNT

        # Functional
        self.yaml = {}
        self.ready_2_print = False
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
                sys.stdout.write('Caught other error: ' + repr(error))
                raise

# ======== FUNCTIONS ======== #
    def make_yaml(self) -> None:
        if self._ready_2_print:
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
                sys.stdout.write('Caught other error: ' + repr(error))
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
        self.ready_2_print = True

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
    def ready_2_print(self) -> bool:
        return self._ready_2_print

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

    @ready_2_print.setter
    def ready_2_print(self, r2p: bool):
        self._ready_2_print = r2p

# ======== CHECKS ======== #
    def check_type(self, _type: str) -> None:
        if _type not in self.PART_TYPES:
            try:
                raise ValueError(f'Problem with _type argument: {_type}')
            except Exception as error:
                sys.stdout.write('Caught other error: ' + repr(error))
                raise

    def check_orientation(self, orientation: int) -> None:
        if orientation not in self.PART_ORIENTATIONS:
            try:
                raise ValueError(
                    f'Problem with orientation argument: {orientation}')
            except Exception as error:
                sys.stdout.write('Caught other error: ' + repr(error))
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
                    sys.stdout.write('Caught other error: ' + repr(error))
                    raise

        temp_params = {self.B: blue, self.G: green, self.R: red}
        if temp_params not in self.ACCEPTED_COLORS:
            try:
                raise ValueError(
                    f'Problem with params argument: {temp_params}')
            except Exception as error:
                sys.stdout.write('Caught other error: ' + repr(error))
                raise

    def check_child(self, direction: int, child: object) -> None:
        if direction not in self.DIRECTIONS:
            try:
                raise ValueError(
                    f'Non-existant direction of child: {direction}')
            except Exception as error:
                sys.stdout.write('Caught other error: ' + repr(error))
                raise
        if isinstance(child, Component) != True:
            try:
                raise ValueError(
                    f'Child must be of class "Component", current is: {type(child)}')
            except Exception as error:
                sys.stdout.write('Caught other error: ' + repr(error))
                raise


class Parser(Module):
    def indx_2_direction(self, child_index: int, compass: Compass) -> list:
        # Out of Node
        if child_index == -1:
            compass.rotate('z', -180)
            return
        elif child_index == -2:
            return
        elif child_index == -3:
            compass.rotate('z', -90)
            return
        elif child_index == -4:
            compass.rotate('z', 90)
            return

        # In to Node
        direction = deepcopy(compass.compass[child_index])
        if child_index == 0:
            compass.rotate('z', 180)
            return direction
        elif child_index == 1:
            return direction
        elif child_index == 2:
            print(direction)
            compass.rotate('z', 90)
            return direction
        elif child_index == 3:
            compass.rotate('z', -90)
        return direction

    def orientation_rotation(self, orientation: int, compass: Compass, undo: bool = False):
        for direction in compass.compass:
            if [1, 0, 0] == compass.compass[direction]:
                if undo == False:
                    if direction == 1:
                        compass.rotate('x', orientation)
                    elif direction == 2:
                        compass.rotate('y', -orientation)
                    elif direction == 3:
                        compass.rotate('y', orientation)
                elif undo == True:
                    if direction == 1:
                        compass.rotate('x', -orientation)
                    elif direction == 2:
                        compass.rotate('y', orientation)
                    elif direction == 3:
                        compass.rotate('y', -orientation)

    def yaml_parser(self, yaml: set, component: Component, compass: Compass, grid: Grid) -> None:
        for child_index in yaml:
            type_ = yaml[child_index][self.TYPE]
            orientation = yaml[child_index][self.ORIENTATION]
            conversion = {
                self.HINGE: 'hinge',
                self.BRICK: 'brick'
            }
            # Form partial id of part
            id_ = f'{conversion[type_]}{orientation}_'

            print()
            print(id_)
            print(compass.compass.items())
            print(child_index)

            # Rotate part by orientation orientation
            if orientation == 90:
                self.orientation_rotation(orientation, compass)

            # Return direction of child
            direction = self.indx_2_direction(child_index, compass)
            print(compass.compass.items())

            new_x = component.x + direction[0]
            new_y = component.y + direction[1]
            new_z = component.z + direction[2]

            new_component = Component(id_, new_x, new_y, new_z)
            component.set_child(child_index, new_component)
            grid.insert_element(new_component.x, new_component.y,
                                new_component.z, new_component, deepcopy(compass))

            # Show Basic View Progression
            # view = grid.get_view()
            # print(view)

            # Catch Leafs
            if self.CHILDREN in yaml[child_index]:
                new_yaml = yaml[child_index][self.CHILDREN]
                self.yaml_parser(new_yaml, new_component, compass, grid)

            __ = self.indx_2_direction((child_index+1)*-1, compass)

            # Undo orientation rotation
            if orientation == 90:
                self.orientation_rotation(orientation, compass, undo = True)


            # # Do Block Rotation
            # depth_dimension = 'x'
            # if orientation == 90:
            #     compass.rotate(depth_dimension, 90)

            # # Rotate Back
            # if orientation == 90:
            #     compass.rotate(depth_dimension, -90)


class Voxel(Button):
    def __init__(self, position=(0, 0, 0)):
        super().__init__(
            parent=scene,
            position=position,
            origin_y=.5,
            color=color.white,
            highlight_color=color.orange,
        )

    # def input(self, key):
    #     if self.hovered:
    #         if key == 'left mouse down':
    #             voxel = Voxel(position=self.position + mouse.normal)
    #         if key == 'right mouse down':
    #             destroy(self)


def main(yaml_file):
    ## WORK WITH DATA ##
    body = yaml_file['body']
    current = body['children']

    # Parameters
    size = 20
    half_size = int(size/2)
    x_center, y_center, z_center = half_size, half_size, half_size

    # Object
    core = Component('core', x=x_center, y=y_center, z=z_center)

    grid = Grid(size, size, size)
    parser = Parser()
    compass = Compass()

    # Initilize Grid
    grid.insert_element(core.x, core.y, core.z, core, deepcopy(compass))

    # Parse YAML
    parser.yaml_parser(current, core, compass, grid)
    # view = grid.get_view()
    # print(view)

    # Get YAML
    core.make_yaml()
    yaml_file = core.yaml

    # Accepted Colors

    # Make Ursina Editor
    part_colors = {'CoreComponent': {0: 'FFFFFF', 90: 'FFFFFF'},
                   'FixedBrick': {0: '1F47FF', 90: 'FFB400'},
                   'ActiveHinge': {0: '94FF00', 90: 'FF0070'}
                   }
    models = {'CoreComponent': 'models/core/core.obj',
              'FixedBrick': 'models/brick/brick.obj',
              'ActiveHinge': 'models/hinge/hinge.obj'
              }

    textures = {'CoreComponent': 'models/core/core_na.png',
                'FixedBrick': 'models/brick/brick_na.png',
                'ActiveHinge': 'models/hinge/hinge_na.png'
                }

    elements = grid.elements

    view = grid.get_view()
    count = 0
    for x in range(0, size):
        for y in range(0, size):
            for z in range(0, size):
                temp = elements[x][y][z]
                if count == 9:
                        continue
                elif 1 in temp:
                    voxel = Voxel()
                    voxel.position = (x-half_size, y-half_size, z-half_size)
                    voxel.color = color.hex(
                        part_colors[temp[1].type_][temp[1].orientation])
                    voxel.model = models[temp[1].type_]
                    voxel.texture = textures[temp[1].type_]

                    print(' ====== STATS ====== ')
                    print(temp[1].id_)
                    print(temp['compass'].compass[1])
                    print(temp['compass'].compass[2])
                    print("------ ANGLES ")
                    theta_x = angle_between(temp['compass'].compass[1], [1, 0, 0]) * -temp['compass'].compass[1][1]
                    theta_y = angle_between(temp['compass'].compass[2], [0, 1, 0]) * -temp['compass'].compass[1][2]
                    print(temp[1].orientation)
                    print(f'x: {theta_x}')
                    print(f'y: {theta_y}')
                    count += 1
                    print()
                    voxel.rotation = [temp[1].orientation, 0.0, theta_x]

    return yaml_file


if __name__ == '__main__':
    # Start Ursina
    app = Ursina()

    ####################

    # Read Input From YAML File
    path = './test.yaml'
    # path = './tardigrade.yaml'
    # path = './phenotypes/phenotype_1.yaml' # Conflicts without z depth rotation
    # path = './phenotypes/phenotype_10.yaml'
    # path = './phenotypes/phenotype_100.yaml'
    # path = './phenotypes/phenotype_228.yaml' # Conflicts without z depth rotation
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

    # Print Output To YAML File
    name = 'out'
    path = ('./' + name + '.yaml')
    with open(path, 'w') as f:
        pyyaml.dump(data, f, sort_keys=False)

    ####################

    hotkeys = {'toggle_orthographic': 'shift+p',
               'focus': 'f', 'reset_center': 'shift+f'}
    EditorCamera()
    app.run()
