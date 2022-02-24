#!/usr/bin/env python3
import yaml

from main_2 import CHILDREN

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

YELLOW = {'b': 0, 'g': 1, 'r': 1}
BLUE = {'b': 1, 'g': 0, 'r': 0}
GREEN = {'b': 0, 'g': 1, 'r': 0}
RED = {'b': 0, 'g': 0, 'r': 1}

def make_part_yaml(part, _id, _type, orientation, b, g, r):
    part[ID] = _id
    part[TYPE] = _type
    part[ORIENTATION] = orientation
    part[PARAMS] = {}
    part[PARAMS][B] = b
    part[PARAMS][G] = g
    part[PARAMS][R] = r
    return part

def make_hinge(part, n):
    _id = f'hinge_{n}'
    return make_part_yaml(part, _id, ACTIVEHINGE, 0, **RED)

def make_hinge_90(part, n):
    _id = f'hinge_{n}'
    return make_part_yaml(part, _id, ACTIVEHINGE, 90, **GREEN)

def make_brick(part, n, orientation=0):
    _id = f'hinge_{n}'
    return make_part_yaml(part, _id, FIXEDBRICK, orientation, **BLUE)



def tardigrade_2(data):
    hinge_count = 0
    block_count = 0

    # Child Set-Up
    data[CHILDREN] = {}

    ## First
    curr_idx = 0
    data[CHILDREN][curr_idx] = {}
    current = data[CHILDREN][curr_idx]
    data[CHILDREN][curr_idx] = make_hinge_90(current, hinge_count)
    hinge_count += 1

    ## Second
    curr_idx = 1
    data[CHILDREN][curr_idx] = {}
    current = data[CHILDREN][curr_idx]
    data[CHILDREN][curr_idx] = make_hinge_90(current, hinge_count)
    hinge_count += 1

    ## Third
    curr_idx = 2
    data[CHILDREN][curr_idx] = {}
    current = data[CHILDREN][curr_idx]
    data[CHILDREN][curr_idx] = make_hinge(current, hinge_count)
    hinge_count += 1

    return data

if __name__ == '__main__':
    # Add Core
    data = {}
    data = make_part_yaml(data, 'Core', CORECOMPONENT, 0, **YELLOW)

    # Recursive Placement Of Children
    data = tardigrade_2(data)

    # Add Header
    top = {}
    top[ID] = 'out'
    top[BODY] = {}
    top[BODY] = data

    ####################

    # Print Output To YAML File
    name = 'out'
    path = ('./' + name + '.yaml')
    with open(path, 'w') as f:
        yaml.dump(top, f, sort_keys=False)
