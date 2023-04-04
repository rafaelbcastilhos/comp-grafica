# -*- coding: utf-8 -*-

from abc import ABC
from enum import Enum
from sgi.transform import Transform, Vector


class ObjectType(Enum):
    NULL = 0
    POINT = 1
    LINE = 2
    RECTANGLE = 3
    POLYGON = 4


class Object(ABC):
    name: str
    color: tuple
    line_width: float
    coords: list[Vector]
    object_type: ObjectType
    normalized_coords: list[Vector]
    fill: bool
    _transform: Transform

    def __init__(self,
                 coords: list,
                 name: str,
                 color: tuple,
                 line_width: float,
                 object_type: ObjectType,
                 fill: bool):
        super().__init__()
        self.name = name
        self.color = color
        self.line_width = line_width
        self.coords = coords
        self.normalized_coords = coords
        self.object_type = object_type
        self.fill = fill
        self._transform = Transform(self.calculate_center(), Vector(0.0, 0.0, 0.0), Vector(1.0, 1.0, 1.0))

    @property
    def position(self):
        return self._transform.position

    @property
    def scale(self):
        return self._transform.scale

    @property
    def rotation(self):
        return self._transform.rotation

    def calculate_center(self):
        coord_sum = Vector(0.0, 0.0, 0.0)

        for coord in self.coords:
            coord_sum += coord

        return coord_sum / len(self.coords)

    def translate(self, direction: Vector, normalized: bool = False):
        if normalized:
            direction = self._transform.rotate(self.rotation.z, [direction + self.position], None, False)[0]
            direction -= self.position

        self.coords = self._transform.translate(direction, self.coords)

    def rescale(self, scale: Vector):
        self.coords = self._transform.rescale(scale, self.coords)

    def rotate(self, angle: float, anchor: Vector = None):
        self.coords = self._transform.rotate(angle, self.coords, anchor)

    def normalize(self, window_center: Vector, window_scale: Vector, window_rotation: float):
        diff_x = 1.0 / window_scale.x
        diff_y = 1.0 / window_scale.y
        diff_z = 1.0 / window_scale.z

        self.normalized_coords = self._transform.normalize(window_center,
                                                           window_rotation,
                                                           Vector(diff_x, diff_y, diff_z),
                                                           self.coords)


class Point(Object):
    def __init__(self, position: Vector, name: str = '', color: tuple = (1.0, 1.0, 1.0)):
        super().__init__([position], name, color, 1.0, ObjectType.POINT, False)

    @property
    def coord(self):
        return self.coords[0]

class Line(Object):
    def __init__(self,
                 position_a: Vector,
                 position_b: Vector,
                 name: str = '',
                 color: tuple = (1.0, 1.0, 1.0),
                 line_width: float = 1.0):

        super().__init__([position_a, position_b], name, color, line_width, ObjectType.LINE, False)

    @property
    def start(self):
        return self.coords[0]

    @property
    def end(self):
        return self.coords[1]

class object(Object):
    def __init__(self,
                 coords: list[Vector],
                 name: str = '',
                 color: tuple = (1.0, 1.0, 1.0),
                 line_width: float = 1.0,
                 object_type: ObjectType = ObjectType.POLYGON,
                 fill: bool = False):

        super().__init__(coords, name, color, line_width, object_type, fill)

class Rectangle(object):
    def __init__(self,
                 origin: Vector,
                 extension: Vector,
                 name: str = '',
                 color: tuple = (1.0, 1.0, 1.0),
                 line_width: float = 1.0,
                 fill: bool = False):

        super().__init__([origin,
                         Vector(origin.x, extension.y),
                         extension,
                         Vector(extension.x, origin.y)],
                         name,
                         color,
                         line_width,
                         ObjectType.RECTANGLE,
                         fill)

    @property
    def origin(self):
        return self.coords[0]

    @property
    def corner_a(self):
        return self.coords[1]

    @property
    def extension(self):
        return self.coords[2]

    @property
    def corner_b(self):
        return self.coords[3]

class Window(Rectangle):
    def __init__(self,
                 origin: Vector,
                 extension: Vector,
                 color: tuple = (0.5, 0.0, 0.5),
                 line_width: float = 2.0):
        super().__init__(origin, extension, "Window", color, line_width, False)

    def calculate_up_vector(self):
        return self.coords[1] - self.coords[0]

    @property
    def normalized_origin(self):
        return self.normalized_coords[0]

    @property
    def normalized_extension(self):
        return self.normalized_coords[2]
