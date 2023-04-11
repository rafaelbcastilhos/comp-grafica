# -*- coding: utf-8 -*-

from math import cos, radians, sin, sqrt, acos
import numpy as np


class Vector():
    x: float
    y: float
    z: float

    _list: list

    def __init__(self, x, y, z: float = 0.0):
        self.x = x
        self.y = y
        self.z = z

    def __repr__(self):
        return f"{self.x:.2f}, {self.y:.2f}, {self.z:.2f}"

    def __str__(self):
        return f"{self.x:.2f}, {self.y:.2f}, {self.z:.2f}"

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y, self.z - other.z)

    def __mul__(self, other):
        result = None
        if isinstance(other, (float, int)):
            result = Vector(self.x * other, self.y * other, self.z * other)
        elif isinstance(other, Vector):
            result = acos(self.dot_product(other) / (self.magnitude() * other.magnitude()))
        else:
            raise NotImplementedError

        return result

    def __truediv__(self, other):
        if isinstance(other, (float, int)):
            return Vector(self.x / other, self.y / other, self.z / other)
        raise NotImplementedError

    def dot_product(self, other):
        return self.x * other.x + self.y * other.y + self.z * other.z

    def magnitude(self):
        return sqrt(self.x**2 + self.y**2 + self.z**2)

class Transform():
    _position: Vector
    _rotation: Vector
    _scale: Vector
    _translation_matrix: np.matrix
    _scaling_matrix: np.matrix
    _rotation_matrix_x: np.matrix
    _rotation_matrix_y: np.matrix
    _rotation_matrix_z: np.matrix
    _normalization_matrix: np.matrix

    def __init__(self,
                 position,
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

        cos_ = cos(rotation.x)
        sin_ = sin(rotation.x)

        self._rotation_matrix_x = np.matrix([[1.0, 0.0, 0.0, 0.0],
                                             [0.0, cos_, sin_, 0.0],
                                             [0.0, sin_, cos_, 0.0],
                                             [0.0, 0.0, 0.0, 1.0]])

        cos_ = cos(rotation.y)
        sin_ = sin(rotation.y)

        self._rotation_matrix_y = np.matrix([[cos_, 0.0, sin_, 0.0],
                                             [0.0, 1.0, 0.0, 0.0],
                                             [-sin_, 0.0, cos_, 0.0],
                                             [0.0, 0.0, 0.0, 1.0]])

        cos_ = cos(rotation.z)
        sin_ = sin(rotation.z)

        self._rotation_matrix_z = np.matrix([[cos_, -sin_, 0.0, 0.0],
                                             [sin_, cos_, 0.0, 0.0],
                                             [0.0, 0.0, 1.0, 0.0],
                                             [0.0, 0.0, 0.0, 1.0]])


        self._normalization_matrix = np.matrix([[cos_ * self._scale.x, -sin_ * self._scale.y, 0.0, self._position.x],
                                                [sin_ * self._scale.x, cos_ * self._scale.y, 0.0, self._position.y],
                                                [0.0, 0.0, self._scale.z, self._position.z],
                                                [0.0, 0.0, 0.0, 1.0]])

    def __repr__(self):
        return str(f"P: {self.position}, S: {self.scale}, R: {self._rotation}")

    def __str__(self):
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

    @staticmethod
    def world_to_local(coord, anchor):
        return coord - anchor

    @staticmethod
    def local_to_world(coord, anchor):
        return coord + anchor

    @staticmethod
    def translate_vector(direction, vector):
        translation_matrix = np.matrix([[1.0, 0.0, 0.0, direction.x],
                                        [0.0, 1.0, 0.0, direction.y],
                                        [0.0, 0.0, 1.0, direction.z],
                                        [0.0, 0.0, 0.0, 1.0]])

        new_vector = np.matmul(translation_matrix, [vector.x, vector.y, vector.z, 1])

        return Vector(new_vector[0, 0], new_vector[0, 1], new_vector[0, 2])

    @staticmethod
    def reescale_vector(scale, vector, anchor):
        scaling_matrix = np.matrix([[scale.x, 0.0, 0.0, 0.0],
                                    [0.0, scale.y, 0.0, 0.0],
                                    [0.0, 0.0, scale.z, 0.0],
                                    [0.0, 0.0, 0.0, 1.0]])

        relative_vector = Transform.world_to_local(vector, anchor)

        new_vector = np.matmul(scaling_matrix, [relative_vector.x, relative_vector.y, relative_vector.z, 1])
        return Transform.local_to_world(Vector(new_vector[0, 0], new_vector[0, 1], new_vector[0, 2]), new_vector)

    @staticmethod
    def rotate_vector(angle, vector, anchor):
        angle_cos = cos(radians(angle))
        angle_sin = sin(radians(angle))

        rotation_matrix_z = np.matrix([[angle_cos, -angle_sin, 0.0, 0.0],
                                       [angle_sin, angle_cos, 0.0, 0.0],
                                       [0.0, 0.0, 1.0, 0.0],
                                       [0.0, 0.0, 0.0, 1.0]])

        relative_vector = Transform.world_to_local(vector, anchor)
        new_vector = np.matmul(rotation_matrix_z, [relative_vector.x, relative_vector.y, relative_vector.z, 1])
        return Transform.local_to_world(Vector(new_vector[0, 0], new_vector[0, 1], new_vector[0, 2]), anchor)

    def translate(self,
                  direction,
                  coords,
                  update_internal_vectors: bool = True):
        if update_internal_vectors:
            self._position += direction

        self._translation_matrix[0, 3] = direction.x
        self._translation_matrix[1, 3] = direction.y
        self._translation_matrix[2, 3] = direction.z

        new_coords = []

        for coord in coords:
            new_coord = np.matmul(self._translation_matrix, [coord.x, coord.y, coord.z, 1])
            new_coords.append(Vector(new_coord[0, 0], new_coord[0, 1], new_coord[0, 2]))

        return new_coords

    def rescale(self,
                scale,
                coords,
                anchor: Vector = None,
                update_internal_vectors: bool = True):
        if update_internal_vectors:
            self._scale.x *= scale.x
            self._scale.y *= scale.y
            self._scale.z *= scale.z

        self._scaling_matrix[0, 0] = scale.x
        self._scaling_matrix[1, 1] = scale.y
        self._scaling_matrix[2, 2] = scale.z

        new_coords = []

        if anchor is None:
            anchor = self._position

        for coord in coords:
            relative_coord = self.world_to_local(coord, anchor)
            new_coord = np.matmul(self._scaling_matrix, [relative_coord.x, relative_coord.y, relative_coord.z, 1])
            relative_new_coord = self.local_to_world(Vector(new_coord[0, 0], new_coord[0, 1], new_coord[0, 2]), anchor)
            new_coords.append(relative_new_coord)

        return new_coords

    def rotate(self,
               angle,
               coords,
               anchor: Vector = None,
               update_internal_vectors: bool = True):
        if update_internal_vectors:
            self._rotation.z = (self._rotation.z + angle) % 360

        angle_cos = cos(radians(angle))
        angle_sin = sin(radians(angle))

        self._rotation_matrix_z[0, 0] = angle_cos
        self._rotation_matrix_z[0, 1] = -angle_sin
        self._rotation_matrix_z[1, 0] = angle_sin
        self._rotation_matrix_z[1, 1] = angle_cos

        corrected_coords = coords + [self._position] if update_internal_vectors else coords
        new_coords = []

        if anchor is None:
            anchor = self._position

        for coord in corrected_coords:
            relative_coord = self.world_to_local(coord, anchor)
            new_coord = np.matmul(self._rotation_matrix_z, [relative_coord.x, relative_coord.y, relative_coord.z, 1])
            relative_new_coord = self.local_to_world(Vector(new_coord[0, 0], new_coord[0, 1], new_coord[0, 2]), anchor)
            new_coords.append(relative_new_coord)

        if update_internal_vectors:
            self._position = new_coords[-1]  # Atualiza a posição
            return new_coords[:-1]  # Retorna todas as coordenadas menos a posição

        return new_coords

    def normalize(self,
                  window_center,
                  window_rotation,
                  scale,
                  coords):
        new_coords = []

        # Translação
        self._normalization_matrix[0, 3] = -window_center.x
        self._normalization_matrix[1, 3] = -window_center.y
        self._normalization_matrix[2, 3] = -window_center.z

        angle_cos = cos(radians(-window_rotation))
        angle_sin = sin(radians(-window_rotation))

        # Escala e rotação
        self._normalization_matrix[0, 0] = angle_cos * scale.x
        self._normalization_matrix[0, 1] = -angle_sin * scale.y
        self._normalization_matrix[1, 0] = angle_sin * scale.x
        self._normalization_matrix[1, 1] = angle_cos * scale.y
        self._normalization_matrix[2, 2] = angle_cos * scale.z

        for coord in coords:
            relative_coord = self.world_to_local(coord, Vector(0.0, 0.0, 0.0))
            new_coord = np.matmul(self._normalization_matrix, [relative_coord.x, relative_coord.y, relative_coord.z, 1])
            relative_new_coord = self.local_to_world(Vector(new_coord[0, 0], new_coord[0, 1], new_coord[0, 2]),
                                                     Vector(0.0, 0.0, 0.0))
            new_coords.append(relative_new_coord)

        return new_coords
