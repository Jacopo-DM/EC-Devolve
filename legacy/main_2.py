#!/usr/bin/env python3
import yaml

# Globals
ACTIVEHINGE = 'ActiveHinge'
FIXEDBRICK = 'FixedBrick'
CORECOMPONENT = 'CoreComponent'
PART_TYPES = [ACTIVEHINGE, FIXEDBRICK, CORECOMPONENT]
PART_ORIENTATIONS = [0, 90]
PART_RGB_VALUES = [0, 1]
YELLOW = {'b': 0, 'g': 1, 'r': 1}
BLUE = {'b': 1, 'g': 0, 'r': 0}
GREEN = {'b': 0, 'g': 1, 'r': 0}
RED = {'b': 0, 'g': 0, 'r': 1}
PART_RGB_OPTIONS = ['100', '010', '001', '011']
ID = 'id'
BODY = 'body'
TYPE = 'type'
ORIENTATION = 'orientation'
PARAMS = 'params'
B = 'blue'
G = 'green'
R = 'red'
CHILDREN = 'children'
ZERO = 0
ONE = 1
TWO = 2
THREE = 3


class Part(object):
    def __init__(self, _id: str, _type: str, orientation: int, b: int, g: int, r: int) -> None:
        # Input Value Checks
        self.check_type(_type)
        self.check_orientation(orientation)
        self.check_params(b, g, r)

        # Set Object Variables
        self.__id = _id
        self.__type = _type
        self.__orientation = orientation
        self.__params = {B: b, G: g, R: r}
        self.__children = {}

        # Things To Add:
        # TODO: More meaningful error messages in checks

    def check_type(self, _type: str) -> None:
        if _type not in PART_TYPES:
            try:
                raise ValueError('Problem with _type argument: {_type}')
            except Exception as error:
                print('Caught other error: ' + repr(error))

    def check_orientation(self, orientation: int) -> None:
        if orientation not in PART_ORIENTATIONS:
            try:
                raise ValueError(
                    'Problem with orientation argument: {orientation}')
            except Exception as error:
                print('Caught other error: ' + repr(error))

    def check_params(self, b: int, g: int, r: int) -> None:
        if b not in PART_RGB_VALUES:
            try:
                raise ValueError('Problem with b argument: {b}')
            except Exception as error:
                print('Caught other error: ' + repr(error))
        if g not in PART_RGB_VALUES:
            try:
                raise ValueError('Problem with g argument: {g}')
            except Exception as error:
                print('Caught other error: ' + repr(error))

        if r not in PART_RGB_VALUES:
            try:
                raise ValueError('Problem with r argument: {r}')
            except Exception as error:
                print('Caught other error: ' + repr(error))

        temp_params = f'{b}{g}{r}'
        if temp_params not in PART_RGB_OPTIONS:
            try:
                raise ValueError('Problem with params argument: {temp_params}')
            except Exception as error:
                print('Caught other error: ' + repr(error))

    def check_children(self, part: object) -> None:
        if isinstance(part, Part) != True:
            try:
                raise ValueError('Child isn\'t instance of Part(): {type(part)}')
            except Exception as error:
                print('Caught other error: ' + repr(error))

    def set_id(self, new_id: str) -> None:
        self.__id = new_id

    def set_type(self, new_type: str) -> None:
        self.check_type(new_type)
        self.__type = new_type

    def set_orientation(self, new_orientation: int) -> None:
        self.check_orientation(new_orientation)
        self.__orientation = new_orientation

    def set_params(self, b: int, g: int, r: int) -> None:
        self.check_params(b, g, r)
        self.__params = {B: b, G: g, R: r}

    def set_children(self, part: object, index: int) -> None:
        self.check_children(part)
        self.__children[index] = part

    def get_id(self) -> str:
        return self.__id

    def get_type(self) -> str:
        return self.__type

    def get_orientation(self) -> int:
        return self.__orientation

    def get_params(self) -> int:
        return self.__params

    def get_yaml(self) -> set:
        section = {ID: self.__id,
                   TYPE: self.__type,
                   ORIENTATION: self.__orientation,
                   PARAMS: self.__params,
                   }
        if self.__children:
            section[CHILDREN] = {}
            for child in self.__children:
                section[CHILDREN][child] = self.__children[child].get_yaml()
        return section


class Robot(object):
    def __init__(self, name: str) -> None:
        # Set Object Variables
        self.id = name
        self.body = None  # Alternative To Children
        self.core = None
        self.core_present = False
        self.parts = []

        # Add Core (Mendatory To All Builds)
        self.__add_core()

    def __add_core(self) -> None:
        if self.core_present == False:
            self.core = Part(_id='Core', _type=CORECOMPONENT,
                             orientation=0, **YELLOW)
            self.core_present == True
        elif self.core_present == True:
            try:
                raise ValueError('Core already exists!')
            except Exception as error:
                print('Caught other error: ' + repr(error))

    def add_part(self, part: object) -> None:
        if isinstance(part, Part):
            if part.get_type() == CORECOMPONENT:  # Stop User From Adding More Cores
                try:
                    raise ValueError('Core already exists!')
                except Exception as error:
                    print('Caught other error: ' + repr(error))
            else:
                self.parts.append(part)
        else:
            raise TypeError

    def make_body(self) -> None:
        self.body = self.core.yamal_out()
        print(self.body)
        for part in self.parts:
            pass

    def yaml_out(self) -> set:
        # Initialize
        robot_yaml = {ID: self.id}

        # Add Body
        self.make_body()
        if self.body != None:
            robot_yaml[BODY] = self.body
        return robot_yaml


def get_yaml(path) -> set:
    with open(path) as f:
        data = yaml.load(f, Loader=yaml.FullLoader)
    return data


class Tree(object):
    def __init__(self, _id):
        self.id = _id
        self.edges = []

def explore_yaml(parts):
    _id = parts[ID]
    _type = parts[TYPE]
    orientation = parts[ORIENTATION]
    b = parts[PARAMS][B]
    g = parts[PARAMS][G]
    r = parts[PARAMS][R]
    children = parts[CHILDREN]
    if _type == CORECOMPONENT:
        core = Part(_id, _type, orientation, b, g, r)
        for child in children:
            core.set_children(explore_yaml(children[child]), child)
        return core
    else:
        return Part(_id, _type, orientation, b, g, r)

    # def __init__(self, _id: str, _type: str, orientation: int, b: int, g: int, r: int) -> None:

        # if items == BODY:
        #     explore_yaml(parts[BODY])
        # if items == CHILDREN:
        #     explore_yaml(parts[CHILDREN])
        # if items == ZERO or items == ONE or items == TWO or items == THREE:
        #     explore_yaml(parts[items])


def print_yaml(parts, indent):
    indentation = indent * "|"
    for items in parts:
        print(f'{indentation}-{items}')
        indent += 1
        if items == BODY:
            print_yaml(parts[BODY], indent=indent)
        if items == CHILDREN:
            print_yaml(parts[CHILDREN], indent=indent)
        if items == ZERO or items == ONE or items == TWO or items == THREE:
            print_yaml(parts[items], indent=indent)
        indent -= 1

if __name__ == '__main__':
    yaml_file = get_yaml('./tardigrade.yaml')
    name = yaml_file[ID]
    yaml_file = yaml_file[BODY]#[CHILDREN]
    indent = 0
    print(print_yaml(yaml_file, indent=indent))

    # yaml_file = explore_yaml(yaml_file)
    # print(yaml_file.get_yaml())
    exit()

    name = 'out'
    robot = Robot(name)
    part_1 = Part('test', ACTIVEHINGE, 0, **BLUE)
    robot.add_part(part_1)

    # Print Output To YAML File
    out = robot.yaml_out()
    with open(f'{name}.yaml', 'w') as f:
        yaml.dump(out, f, sort_keys=False)
