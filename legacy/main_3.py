#!/usr/bin/env python3
import yaml
import numpy as np

ACTIVEHINGE = 'ActiveHinge'
FIXEDBRICK = 'FixedBrick'
CORECOMPONENT = 'CoreComponent'
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
X = 'x'
Y = 'y'
CHILDS = [0, 1, 2, 3]
NORTH = 'north'
EAST = 'east'
SOUTH = 'south'
WEST = 'west'
DIRECTION_INV = {
    0: SOUTH,
    1: NORTH,
    2: EAST,
    3: WEST,
}
SIZE_X, SIZE_Y = 20, 20
CENTER_X, CENTER_Y = int(SIZE_X/2), int(SIZE_Y/2)
HEAD_X, HEAD_Y = CENTER_X, CENTER_Y
VIEW_GRID = np.zeros([SIZE_X, SIZE_Y])


def make_part_yaml(part, _id, _type, orientation, b, g, r):
    part[ID] = _id
    part[TYPE] = _type
    part[ORIENTATION] = orientation
    part[PARAMS] = {}
    part[PARAMS][B] = b
    part[PARAMS][G] = g
    part[PARAMS][R] = r
    return part


def get_part_config(current):
    _id = current[ID].capitalize()
    _type = current[TYPE]
    orientation = current[ORIENTATION]
    b = current[PARAMS][B]
    g = current[PARAMS][G]
    r = current[PARAMS][R]
    return _id, _type, orientation, b, g, r


def make_children_yaml(current, part):
    global HEAD_X, HEAD_Y, VIEW_GRID
    for child in current:
        # Make & Set Children
        _id, _type, orientation, b, g, r = get_part_config(current[child])
        part[CHILDREN][child] = make_part_yaml({}, _id, _type, orientation, b, g, r)

        # Recur
        try:
            current[child][CHILDREN]
        except KeyError:
            continue
        part[CHILDREN][child][CHILDREN] = {}
        new_current = current[child][CHILDREN]
        make_children_yaml(new_current, part[CHILDREN][child])

def print_yaml(parts, indent):
    indentation = indent * "|"
    for items in parts:
        if items == TYPE or items == ORIENTATION:
            print(f'{indentation}-{parts[items]}')
        if items in CHILDS:
            print(f'{indentation}-{DIRECTION_INV[items]}')
        indent += 1
        if items == BODY:
            print_yaml(parts[BODY], indent=indent)
        if items == CHILDREN:
            print_yaml(parts[CHILDREN], indent=indent)
        if items == ZERO or items == ONE or items == TWO or items == THREE:
            print_yaml(parts[items], indent=indent)
        indent -= 1
def yaml_parser(yaml, x, y):
    for child in yaml:
        edge = False
        if child in [0, 1, 2, 3]:
            new_x, new_y = coordinator(child, x, y)
            edge = True
        elif child == CHILDREN:
            new_x = x
            new_y = y
            edge = True
        if edge:
            VIEW_GRID[x, y] = 1
            yaml_parser(yaml[child], new_x, new_y)
            # print(child)

def coordinator(val, x, y):
    if val == 0:
        return x, y+1
    if val == 1:
        return x, y-1
    if val == 2:
        return x-1, y
    if val == 3:
        return x+1, y

if __name__ == '__main__':
    # Read Input From YAML File
    name = 'phenotype_6'
    path = ('./phenotypes/' + name + '.yaml')
    with open(path) as f:
        data = yaml.load(f, Loader=yaml.FullLoader)

    ## WORK WITH DATA ##m
    current = data[BODY][CHILDREN]
    # x=CENTER_X
    # y=CENTER_Y
    # VIEW_GRID[x, y] = 1
    # VIEW_GRID[x+1, y] = 4
    # VIEW_GRID[x, y+1] = 1
    # VIEW_GRID[x-1, y] = 3
    # VIEW_GRID[x, y-1] = 2
    yaml_parser(current, x=CENTER_X, y=CENTER_Y)
    print(VIEW_GRID)
    exit()


    # # yaml_file = data[BODY]#[CHILDREN]
    # # indent = 1
    # # compact = print_yaml(yaml_file, indent)

    # # Add Core
    # sample = {}
    # sample = make_part_yaml(sample, 'Core', CORECOMPONENT, 0, 0, 1, 1)

    # # Recursive Placement Of Children
    # sample[CHILDREN] = {}
    # current = data[BODY][CHILDREN]
    # make_children_yaml(current, sample)

    # Add Header
    top = {}
    top[ID] = 'out'
    top[BODY] = {}
    top[BODY] = current

    print(VIEW_GRID)
    data = top

    ####################

    # Print Output To YAML File
    name = 'out'
    path = ('./' + name + '.yaml')
    with open(path, 'w') as f:
        yaml.dump(data, f, sort_keys=False)
