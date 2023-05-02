# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod
from enum import Enum
import numpy as np
from sgi.transform import Transform, Vector


class ObjectType(Enum):
    NULL = 0
    POINT = 1
    LINE = 2
    RECTANGLE = 4
    POLYGON = 5
    POLYGON3D = 6
    BEZIER_CURVE = 7
    SPLINE_CURVE = 8
    PARALLELEPIPED = 9

class Object(ABC):
    name: str
    color: tuple
    line_width: float
    coords: list[Vector]
    object_type: ObjectType
    normalized_coords: list[Vector]
    projected_coords: list[Vector]
    lines: list[list[Vector]]
    fill: bool
    closed: bool
    _transform: Transform

    def __init__(self, coords, name, color, line_width, object_type, fill, closed):
        super().__init__()
        self.name = name
        self.color = color
        self.line_width = line_width
        self.coords = coords
        self.normalized_coords = coords
        self.projected_coords = coords
        self.lines = []
        self.object_type = object_type
        self.fill = fill
        self.closed = closed
        self._transform = Transform(self.calculate_center(), Vector(0.0, 0.0, 0.0), Vector(1.0, 1.0, 1.0))
        self.generate_lines()

    @property
    def position(self):
        return self._transform.position

    @property
    def scale(self):
        return self._transform.scale

    @property
    def rotation(self):
        return self._transform.rotation

    @abstractmethod
    def generate_lines(self) -> None:
        '''
        Retorna a representação em linhas.
        '''

    def calculate_center(self):
        coord_sum = Vector(0.0, 0.0, 0.0)

        for coord in self.coords:
            coord_sum += coord

        return coord_sum / len(self.coords)

    def translate(self, direction, normalized: bool = False):
        if normalized:
            direction = self._transform.rotate(self.rotation, [direction + self.position], None, False)[0]
            direction -= self.position

        self.coords = self._transform.translate(direction, self.coords)

    def rescale(self, scale):
        self.coords = self._transform.rescale(scale, self.coords)

    def rotate(self, rotation, anchor: Vector = None) -> None:
        self.coords = self._transform.rotate(rotation, self.coords, anchor)

    def normalize(self, window_center, window_scale, window_rotation):
        diff_x = 1.0 / window_scale.x
        diff_y = 1.0 / window_scale.y
        diff_z = 1.0 / window_scale.z

        self.normalized_coords = self._transform.normalize(window_center,
                                                           window_rotation,
                                                           Vector(diff_x, diff_y, diff_z),
                                                           self.projected_coords)
        self.generate_lines()

    def project(self, cop: Vector, normal: Vector) -> None:
        self.projected_coords = self._transform.project(cop, normal, self.coords)

class Point(Object):
    def __init__(self, position, name: str = '', color: tuple = (1.0, 1.0, 1.0)):
        super().__init__([position], name, color, 1.0, ObjectType.POINT, False, False)

    @property
    def coord(self):
        return self.coords[0]

    def generate_lines(self):
        self.lines = [self.normalized_coords[0], Vector(self.normalized_coords[0].x + 1, self.normalized_coords[0].y)]

class Line(Object):
    def __init__(self,
                 position_a,
                 position_b,
                 name: str = '',
                 color: tuple = (1.0, 1.0, 1.0),
                 line_width: float = 1.0):
        super().__init__([position_a, position_b], name, color, line_width, ObjectType.LINE, False, False)

    @property
    def start(self):
        return self.coords[0]

    @property
    def end(self):
        return self.coords[1]

    def generate_lines(self) -> list[list[Vector]]:
        self.lines = [self.normalized_coords[0], self.normalized_coords[1]]

class Wireframe2D(Object):
    def __init__(self,
                 coords,
                 name: str = '',
                 color: tuple = (1.0, 1.0, 1.0),
                 line_width: float = 1.0,
                 object_type: ObjectType = ObjectType.POLYGON,
                 fill: bool = False):

        super().__init__(coords, name, color, line_width, object_type, fill, True)


    def generate_lines(self):
        lines = []

class Rectangle(Wireframe2D):
    def __init__(self,
                 origin,
                 extension,
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

    def generate_lines(self) -> None:
        lines = []

        for i in range(len(self.normalized_coords) - 1):
            lines.append([self.normalized_coords[i], self.normalized_coords[i + 1]])

        self.lines = lines

class Window(Rectangle):
    cop: Vector
    projected_position: Vector

    def __init__(self,
                 origin,
                 extension,
                 cop,
                 color: tuple = (0.5, 0.0, 0.5),
                 line_width: float = 2.0):
        super().__init__(origin, extension, "Window", color, line_width, False)
        self.cop = cop
        self.projected_cop = self.cop
        self.projected_position = self.position

    def calculate_up_vector(self):
        self.cop = cop
        self.projected_position = self.position

    @property
    def normalized_origin(self) -> Vector:
        return self.normalized_coords[0]

    @property
    def normalized_extension(self) -> Vector:
        return self.normalized_coords[2]

    def calculate_x_axis(self) -> Vector:
        return self.coords[2] - self.coords[1]

    def calculate_y_vector(self) -> Vector:
        return self.coords[1] - self.coords[0]

    def calculate_z_vector(self) -> Vector:
        return (self.calculate_x_axis() / 2.0).cross_product(self.calculate_y_vector() / 2.0)

    def calculate_x_projected_axis(self) -> Vector:
        return self.projected_coords[2] - self.projected_coords[1]

    def calculate_y_projected_vector(self) -> Vector:
        return self.projected_coords[1] - self.projected_coords[0]

    def calculate_z_projected_vector(self) -> Vector:
        return (self.calculate_x_projected_axis() / 2.0).cross_product(self.calculate_y_projected_vector() / 2.0)

    def calculate_cop_distance(self) -> float:
        return (self.projected_position - self.projected_cop).magnitude()

    def translate(self, direction: Vector, normalized: bool = False) -> None:
        if normalized:
            direction = self._transform.rotate(self.rotation, [direction + self.position], None, False)[0]
            direction -= self.position

        coords = self._transform.translate(direction, self.coords + [self.cop])
        self.coords = coords[:-1]
        self.cop = coords[-1]

    def rescale(self, scale: Vector) -> None:
        coords = self._transform.rescale(scale, self.coords + [self.cop])
        self.coords = coords[:-1]
        self.cop = coords[-1]

    def rotate(self, rotation: Vector, anchor: Vector = None) -> None:
        coords = self._transform.rotate(rotation, self.coords + [self.cop], anchor)
        self.coords = coords[:-1]
        self.cop = coords[-1]

    def project(self, cop, normal):
        coords = self._transform.project(cop, normal, self.coords + [cop, self.position])
        self.projected_coords = coords[:-2]
        self.cop = coords[-2]
        self.projected_position = coords[-1]

class BezierCurve(Object):
    _curve_points: list[tuple[Vector]]

    def __init__(self,
                 curve_points: list[Vector],
                 steps: int,
                 name: str = '',
                 color: tuple = (1.0, 1.0, 1.0),
                 line_width: float = 1.0):

        self._curve_points = []
        curve_coords = []

        for i in range(0, len(curve_points), 3):
            if i == len(curve_points) - 1:
                break

            self._curve_points.append((curve_points[i], curve_points[i + 1], curve_points[i + 2], curve_points[i + 3]))
            curve_coords += self.generate_curve_coords(curve_points[i],
                                                       curve_points[i + 1: i + 3],
                                                       curve_points[i + 3],
                                                       steps)

        super().__init__(curve_coords, name, color, line_width, ObjectType.BEZIER_CURVE, False, False)

    def generate_curve_coords(self, start: Vector, control_points: list[Vector], end: Vector, steps: int):
        bezier_points_x = np.matrix([[start.x], [control_points[0].x], [control_points[1].x], [end.x]])
        bezier_points_y = np.matrix([[start.y], [control_points[0].y], [control_points[1].y], [end.y]])

        bezier_matrix = np.matrix([[-1, 3, -3, 1],
                                   [3, -6, 3, 0],
                                   [-3, 3, 0, 0],
                                   [1, 0, 0, 0]])

        curve = []

        for step in range(steps):
            t = step / steps
            step_matrix = np.matrix([t**3, t**2, t, 1])
            new_x = step_matrix * bezier_matrix * bezier_points_x
            new_y = step_matrix * bezier_matrix * bezier_points_y
            curve.append(Vector(new_x[0, 0], new_y[0, 0], 0.0))

        return curve


class SplineCurve(Object):
    def __init__(self,
                 spline_points: list,
                 fill: bool,
                 closed: bool,
                 steps: int,
                 name: str = '',
                 color: tuple = (1.0, 1.0, 1.0),
                 line_width: float = 1.0,
                 forward_diff: bool = True) -> None:

        spline_coords = []

        if forward_diff:
            spline_coords = self.generate_spline_coords_fwd(spline_points, steps, closed)
        else:
            spline_coords = self.generate_spline_coords(spline_points, steps, closed)

        super().__init__(spline_coords, name, color, line_width, ObjectType.SPLINE_CURVE, fill, closed)

    def generate_lines(self) -> None:

        lines = []

        for i, _ in enumerate(self.normalized_coords):
            if i < len(self.normalized_coords) - 1:
                lines.append([self.normalized_coords[i], self.normalized_coords[i + 1]])

        if self.closed:
            lines.append([self.normalized_coords[-1], self.normalized_coords[0]])

        self.lines = lines

    def generate_spline_coords_fwd(self, points: list[Vector], steps: int, closed: bool):
        spline_coords = []

        b_spline_matrix = (1 / 6) * np.matrix([[-1, 3, -3, 1],
                                               [3, -6, 3, 0],
                                               [-3, 0, 3, 0],
                                               [1, 4, 1, 0]])

        delta = 1.0 / steps

        diff_matrix = np.matrix([[0, 0, 0, 1],
                                 [delta**3, delta**2, delta, 0],
                                 [6 * delta**3, 2 * delta**2, 0, 0],
                                 [6 * delta**3, 0, 0, 0]])

        for i, _ in enumerate(points):
            geometry_matrix_x = None
            geometry_matrix_y = None

            if i + 3 < len(points):
                geometry_matrix_x = np.matrix([[points[i].x], [points[i + 1].x], [points[i + 2].x], [points[i + 3].x]])
                geometry_matrix_y = np.matrix([[points[i].y], [points[i + 1].y], [points[i + 2].y], [points[i + 3].y]])
            else:
                if closed:
                    points_len = len(points)
                    index_a = i % points_len
                    index_b = (i + 1) % points_len
                    index_c = (i + 2) % points_len
                    index_d = (i + 3) % points_len

                    geometry_matrix_x = np.matrix([[points[index_a].x],
                                                   [points[index_b].x],
                                                   [points[index_c].x],
                                                   [points[index_d].x]])

                    geometry_matrix_y = np.matrix([[points[index_a].y],
                                                   [points[index_b].y],
                                                   [points[index_c].y],
                                                   [points[index_d].y]])
                else:
                    break

            coeff_matrix_x = b_spline_matrix * geometry_matrix_x
            coeff_matrix_y = b_spline_matrix * geometry_matrix_y

            initial_conditions_matrix_x = diff_matrix * coeff_matrix_x
            initial_conditions_matrix_y = diff_matrix * coeff_matrix_y

            new_x = initial_conditions_matrix_x[0, 0]
            new_y = initial_conditions_matrix_y[0, 0]

            delta_x = initial_conditions_matrix_x[1, 0]
            delta2_x = initial_conditions_matrix_x[2, 0]
            delta3_x = initial_conditions_matrix_x[3, 0]

            delta_y = initial_conditions_matrix_y[1, 0]
            delta2_y = initial_conditions_matrix_y[2, 0]
            delta3_y = initial_conditions_matrix_y[3, 0]

            spline_coords.append(Vector(new_x, new_y, 0.0))

            for _ in range(steps):
                new_x += delta_x
                new_y += delta_y

                delta_x += delta2_x
                delta_y += delta2_y

                delta2_x += delta3_x
                delta2_y += delta3_y

                spline_coords.append(Vector(new_x, new_y, 0.0))

        return spline_coords

    def generate_spline_coords(self, points: list[Vector], steps: int, closed: bool):
        b_spline_matrix = (1 / 6) * np.matrix([[-1, 3, -3, 1],
                                               [3, -6, 3, 0],
                                               [-3, 0, 3, 0],
                                               [1, 4, 1, 0]])
        spline_coords = []

        for i, _ in enumerate(points):
            geometry_matrix_x = None
            geometry_matrix_y = None

            if i + 3 < len(points):
                geometry_matrix_x = np.matrix([[points[i].x], [points[i + 1].x], [points[i + 2].x], [points[i + 3].x]])
                geometry_matrix_y = np.matrix([[points[i].y], [points[i + 1].y], [points[i + 2].y], [points[i + 3].y]])
            else:
                if closed:
                    points_len = len(points)
                    index_a = i % points_len
                    index_b = (i + 1) % points_len
                    index_c = (i + 2) % points_len
                    index_d = (i + 3) % points_len

                    geometry_matrix_x = np.matrix([[points[index_a].x],
                                                   [points[index_b].x],
                                                   [points[index_c].x],
                                                   [points[index_d].x]])

                    geometry_matrix_y = np.matrix([[points[index_a].y],
                                                   [points[index_b].y],
                                                   [points[index_c].y],
                                                   [points[index_d].y]])
                else:
                    break

            for step in range(steps):
                t = step / steps
                step_matrix = np.matrix([t**3, t**2, t, 1])
                new_x = step_matrix * b_spline_matrix * geometry_matrix_x
                new_y = step_matrix * b_spline_matrix * geometry_matrix_y
                spline_coords.append(Vector(new_x[0, 0], new_y[0, 0], 0.0))

        return spline_coords

class Wireframe3D(Object):
    _lines_indexes: list[tuple[int]]

    def __init__(self,
                 coords: list[Vector],
                 line_indexes: list[list[Vector]],
                 name: str = '',
                 color: tuple = (1.0, 1.0, 1.0),
                 line_width: float = 1.0,
                 object_type: ObjectType = ObjectType.POLYGON3D) -> None:

        self._lines_indexes = line_indexes
        super().__init__(coords, name, color, line_width, object_type, False, True)

    def generate_lines(self) -> None:
        lines = []
        for i, j in self._lines_indexes:
            lines.append([self.normalized_coords[i], self.normalized_coords[j]])

        self.lines = lines


class Parallelepiped(Wireframe3D):
    def __init__(self,
                 origin: Vector,
                 extension: Vector,
                 name: str = '',
                 color: tuple = (1.0, 1.0, 1.0),
                 line_width: float = 1.0) -> None:

        coords = []
        line_indexes = []

        coords.append(origin)
        coords.append(Vector(origin.x, extension.y))
        coords.append(extension)
        coords.append(Vector(extension.x, origin.y))

        coords.append(origin + Vector(0.0, 0.0, extension.x - origin.x))
        coords.append(Vector(origin.x, extension.y, extension.x - origin.x))
        coords.append(extension + Vector(0.0, 0.0, extension.x - origin.x))
        coords.append(Vector(extension.x, origin.y, extension.x - origin.x))

        line_indexes.append((0, 1))
        line_indexes.append((1, 2))
        line_indexes.append((2, 3))
        line_indexes.append((3, 0))

        line_indexes.append((0, 4))
        line_indexes.append((1, 5))
        line_indexes.append((2, 6))
        line_indexes.append((3, 7))

        line_indexes.append((4, 5))
        line_indexes.append((5, 6))
        line_indexes.append((6, 7))
        line_indexes.append((7, 4))

        super().__init__(coords, line_indexes, name, color, line_width, ObjectType.PARALLELEPIPED)
