#!/usr/bin/env python3
import numpy as np
from math import radians, degrees


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
    a, b = (vec1 / np.linalg.norm(vec1)).reshape(3), (vec2 / np.linalg.norm(vec2)).reshape(3)
    v = np.cross(a, b)
    c = np.dot(a, b)
    s = np.linalg.norm(v)
    kmat = np.array([[0, -v[2], v[1]], [v[2], 0, -v[0]], [-v[1], v[0], 0]])
    rotation_matrix = np.eye(3) + kmat + kmat.dot(kmat) * ((1 - c) / (s ** 2))
    return rotation_matrix

def get_cardinal_vectors(compass: np.array) -> list:
    # Y-Axis
    zero = np.negative(compass[1, :]).squeeze()
    one = compass[1, :].squeeze()

    # X-Axis
    two = compass[0, :].squeeze()
    three = np.negative(compass[0, :]).squeeze()

    # Z-Axis
    # up = compass[2, :].flatten()
    # down = np.negative(compass[2, :].flatten())

    return [zero, one, two, three]

def rotate_90(compass: np.array):
    return compass.dot(Ry(radians(90)))

def main():
    compass = np.eye(3)
    __, one, two, __ = get_cardinal_vectors(compass)
    one_2_two = rotation_matrix_from_vectors(two, one)
    print(compass.dot(one_2_two))
    one_2_two = rotation_matrix_from_vectors(one, two)
    print(compass.dot(one_2_two))

    print('---')
    print(compass)

    compass = rotate_90(compass)
    print(compass)
    compass = rotate_90(compass)
    print(compass)

    __, one, two, __ = get_cardinal_vectors(compass)
    one_2_two = rotation_matrix_from_vectors(two, one)
    compass = compass.dot(one_2_two)
    print(compass)

if __name__ == '__main__':
    main()
