# -*- coding: utf-8 -*-

from abc import ABC
from enum import Enum
from sgi.transform import Transform, Vector


class ObjectType(Enum):
    NULL = 0
    POINT = 1
    LINE = 2
    TRIANGLE = 3
    RECTANGLE = 4
    POLYGON = 5


class Object(ABC):
    name: str
    color: tuple
    line_width: float
    coord_list: list[Vector]
    object_type: ObjectType
    _transform: Transform

    def __init__(self, coord_list: list, name: str, color: tuple, line_width: float, object_type: ObjectType):
        super().__init__()
        self.name = name
        self.color = color
        self.line_width = line_width
        self.coord_list = coord_list
        self.object_type = object_type
        self._transform = Transform(self.center(), Vector(0.0, 0.0, 0.0), Vector(1.0, 1.0, 1.0))

    @property
    def position(self):
        return self._transform.position

    @property
    def scale(self):
        return self._transform.scale

    @property
    def rotation(self):
        return self._transform.rotation

    def center(self):
        coord_sum = Vector(0.0, 0.0, 0.0)

        for coord in self.coord_list:
            coord_sum += coord

        return coord_sum / len(self.coord_list)

    def translate(self, translation: Vector):
        self.coord_list = self._transform.translate(translation, self.coord_list)

    def rescale(self, scale: Vector):
        self.coord_list = self._transform.rescale(scale, self.coord_list)

    def rotate(self, angle: float, anchor: Vector = None):
        self.coord_list = self._transform.rotate(angle, self.coord_list, anchor)


class Point(Object):
    def __init__(self, position: Vector, name: str = '', color: tuple = (1.0, 1.0, 1.0)):
        super().__init__([position], name, color, 1.0, ObjectType.POINT)

    @property
    def coord(self):
        return self.coord_list[0]

class Line(Object):
    def __init__(self,
                 position_a: Vector,
                 position_b: Vector,
                 name: str = '',
                 color: tuple = (1.0, 1.0, 1.0),
                 line_width: float = 1.0):

        super().__init__([position_a, position_b], name, color, line_width, ObjectType.LINE)

    @property
    def start(self):
        return self.coord_list[0]

    @property
    def end(self):
        return self.coord_list[1]

class Wireframe(Object):
    def __init__(self,
                 coords: list[Vector],
                 name: str = '',
                 color: tuple = (1.0, 1.0, 1.0),
                 line_width: float = 1.0,
                 object_type: ObjectType = ObjectType.POLYGON):

        super().__init__(coords, name, color, line_width, object_type)

class Rectangle(Wireframe):
    def __init__(self,
                 origin: Vector,
                 extension: Vector,
                 name: str = '',
                 color: tuple = (1.0, 1.0, 1.0),
                 line_width: float = 1.0):

        super().__init__(
            [origin, Vector(origin.x, extension.y), extension, Vector(extension.x, origin.y)],
            name, color, line_width, ObjectType.RECTANGLE)

    @property
    def origin(self):
        return self.coord_list[0]

    @property
    def corner_a(self):
        return self.coord_list[1]

    @property
    def extension(self):
        return self.coord_list[2]

    @property
    def corner_b(self):
        return self.coord_list[3]