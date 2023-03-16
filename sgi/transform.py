# -*- coding: utf-8 -*-

from math import cos, radians, sin
import numpy as np


class Vector():
    x: float
    y: float
    z: float

    _list: list

    def __init__(self, x: float, y: float, z: float = 0.0):
        self.x = x
        self.y = y
        self.z = z

    def __repr__(self) :
        return f"{self.x:.2f}, {self.y:.2f}, {self.z:.2f}"

    def __str__(self) :
        return f"{self.x:.2f}, {self.y:.2f}, {self.z:.2f}"

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y, self.z - other.z)

    def __mul__(self, other):
        if isinstance(other, (float, int)):
            return Vector(self.x * other, self.y * other, self.z * other)
        raise NotImplementedError

    def __truediv__(self, other):
        if isinstance(other, (float, int)):
            return Vector(self.x / other, self.y / other, self.z / other)
        raise NotImplementedError


class Transform():
    _position: Vector
    _rotation: Vector
    _scale: Vector
    _translation_matrix: np.matrix
    _scaling_matrix: np.matrix
    _rotation_matrix_x: np.matrix
    _rotation_matrix_y: np.matrix
    _rotation_matrix_z: np.matrix

    def __init__(self,
                 position: Vector,
                 rotation: Vector = Vector(0.0, 0.0, 0.0),
                 scale: Vector = Vector(1.0, 1.0, 1.0)):
        self._position = position
        self._rotation = rotation
        self._scale = scale

        self._translation_matrix = np.matrix([[1.0, 0.0, 0.0, self._position.x],
                                              [0.0, 1.0, 0.0, self._position.y],
                                              [0.0, 0.0, 1.0, self._position.z],
                                              [0.0, 0.0, 0.0, 1.0]])

        self._scaling_matrix = np.matrix([[self._scale.x, 0.0, 0.0, 0.0],
                                          [0.0, self._scale.y, 0.0, 0.0],
                                          [0.0, 0.0, self._scale.z, 0.0],
                                          [0.0, 0.0, 0.0, 1.0]])

        cos_0 = cos(rotation.x)
        sin_0 = sin(rotation.x)

        self._rotation_matrix_x = np.matrix([[1.0, 0.0, 0.0, 0.0],
                                             [0.0, cos_0, sin_0, 0.0],
                                             [0.0, sin_0, cos_0, 0.0],
                                             [0.0, 0.0, 0.0, 1.0]])

        cos_0 = cos(rotation.y)
        sin_0 = sin(rotation.y)

        self._rotation_matrix_y = np.matrix([[cos_0, 0.0, sin_0, 0.0],
                                            [0.0, 1.0, 0.0, 0.0],
                                            [-sin_0, 0.0, cos_0, 0.0],
                                            [0.0, 0.0, 0.0, 1.0]])

        cos_0 = cos(rotation.z)
        sin_0 = sin(rotation.z)

        self._rotation_matrix_z = np.matrix([[cos_0, -sin_0, 0.0, 0.0],
                                            [sin_0, cos_0, 0.0, 0.0],
                                            [0.0, 0.0, 1.0, 0.0],
                                            [0.0, 0.0, 0.0, 1.0]])


    def __repr__(self) :
        return str(f"P: {self.position}, S: {self.scale}, R: {self._rotation}")

    def __str__(self) :
        return str(f"P: {self.position}, S: {self.scale}, R: {self._rotation}")

    @property
    def position(self):
        return self._position

    @property
    def scale(self):
        return self._scale

    @property
    def rotation(self):
        return self._rotation

    def coords_to_local(self, coord: Vector, anchor: Vector = None):
        if anchor is None:
            return coord - self.position
        else:
            return coord - anchor

    def local_to_coords(self, coord: Vector, anchor: Vector = None):
        if anchor is None:
            return coord + self.position
        else:
            return coord + anchor

    def translate(self, direction: Vector, coord_list: list[Vector]):
        self._position += direction

        self._translation_matrix[0, 3] = direction.x
        self._translation_matrix[1, 3] = direction.y
        self._translation_matrix[2, 3] = direction.z

        new_coord_list = []

        # Translação de coordenadas
        for coord in coord_list:

            new_coord = np.matmul(self._translation_matrix, [coord.x, coord.y, coord.z, 1])
            new_coord_list.append(Vector(new_coord[0, 0], new_coord[0, 1], new_coord[0, 2]))

        return new_coord_list

    def rescale(self, scale: Vector, coord_list: list[Vector]):
        # Transformação de escala.
        self._scale.x *= scale.x
        self._scale.y *= scale.y
        self._scale.z *= scale.z

        self._scaling_matrix[0, 0] = scale.x
        self._scaling_matrix[1, 1] = scale.y
        self._scaling_matrix[2, 2] = scale.z

        new_coord_list = []

        # Translação coordenadas
        for coord in coord_list:
            relative_coord = self.coords_to_local(coord)
            new_coord = np.matmul(self._scaling_matrix, [relative_coord.x, relative_coord.y, relative_coord.z, 1])
            relative_new_coord = self.local_to_coords(Vector(new_coord[0, 0], new_coord[0, 1], new_coord[0, 2]))
            new_coord_list.append(relative_new_coord)

        return new_coord_list

    def rotate(self, angle: float, coord_list: list[Vector], anchor: Vector = None):
        # Rotaciona o objeto em relação à um ponto.
        self._rotation.z = (self._rotation.z + angle) % 360

        angle_cos = cos(radians(angle))
        angle_sin = sin(radians(angle))

        self._rotation_matrix_z[0, 0] = angle_cos
        self._rotation_matrix_z[0, 1] = -angle_sin
        self._rotation_matrix_z[1, 0] = angle_sin
        self._rotation_matrix_z[1, 1] = angle_cos

        new_coord_list = []

        for coord in coord_list + [self._position]:
            relative_coord = self.coords_to_local(coord, anchor)
            new_coord = np.matmul(self._rotation_matrix_z, [relative_coord.x, relative_coord.y, relative_coord.z, 1])
            relative_new_coord = self.local_to_coords(Vector(new_coord[0, 0], new_coord[0, 1], new_coord[0, 2]), anchor)
            new_coord_list.append(relative_new_coord)

        self._position = new_coord_list[-1]  # Atualiza a posição

        return new_coord_list[:-1]