#!/usr/bin/env python3
import yaml


class Cube:
    def __init__(self) -> None:
        pass


class Grid(object):
    def __init__(self, x_dim: int, y_dim: int, z_dim: int) -> None:
        # Grid Dimensions
        self._dim_x = x_dim
        self._dim_y = y_dim
        self._dim_z = z_dim

        # Build Grid
        # self.positions = x_dim
        # self.grid  = x_dim

    # def __set_positions(self) -> None:
    #     for x in range(0, self._x_dim):
    #         self._positions[x] = {}
    #         for y in range(0, self._y_dim):
    #             self._positions[x][y] = {}
    #             for z in range(0, self._z_dim):
    #                 self._positions[x][y][z] = 0

    # def __set_grid(self) -> None:
    #     pass

    # ======= PROPERTIES ======= #
    # X Dimension
    # @property
    # def grid(self) -> list:
    #     return self._grid

    # @property.setter
    # def grid(self, x_dim: int) -> None:
    #     self._grid = x_dim

    # @property
    # def positions(self) -> dict:
    #     return self._positions

    # @property.setter
    # def positions(self, x_dim: int, y_dim: int, z_dim: int) -> None:
    #     positions = {}
    #     for x in range(0, x_dim):
    #         positions[x] = {}
    #         for y in range(0, y_dim):
    #             positions[x][y] = {}
    #             for z in range(0, z_dim):
    #                 positions[x][y][z] = 0
    #     self._positions = positions

    # @property.setter
    # def positions(self, x_dim: int, y_dim: int, z_dim: int) -> None:
    #     self._positions = x_dim

    # @property
    # def grid(self) -> dict:
    #     return self._positions

    @property
    def size(self) -> list:
        return [self._x_dim, self._y_dim, self._z_dim]

    # X Dimension
    @property
    def x_dim(self) -> list:
        return self._dim_x

    @property.setter
    def x_dim(self, x_dim: int) -> None:
        self.check_dim(x_dim)
        self._dim_x = x_dim

    # Y Dimension
    @property
    def y_dim(self) -> list:
        return self._dim_y

    @property.setter
    def y_dim(self, y_dim: int) -> None:
        self.check_dim(y_dim)
        self._dim_y = y_dim

    # Z Dimension
    @property
    def z_dim(self) -> list:
        return self._dim_z

    @property.setter
    def z_dim(self, z_dim: int) -> None:
        self.check_dim(z_dim)
        self._dim_z = z_dim

    # ======= CHECKS ======= #
    def check_dim(self, dim: int) -> None:
        if dim <= 0:
            try:
                raise ValueError(
                    'Dimension Can\'t Be Negative or Zero! : {ARG}')
            except Exception as error:
                print('Caught other error: ' + repr(error))


class Component:
    def __init__(self) -> None:
        # Spatial Position
        self._x = None
        self._z = None
        self._y = None

        # Attachment Hinges
        self._east = None   # 0
        self._west = None   # 1
        self._north = None  # 2
        self._south = None  # 3

        # Block Orientation / Rotation
        self._orientation = None

    def toggle_axis(self) -> None:
        pass


if __name__ == '__main__':
    grid = Grid(10, 10, 1)
    print(grid.size)
    # print(grid.grid)
    print(grid.positions)
