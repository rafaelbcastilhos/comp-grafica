# -*- coding: utf-8 -*-

from enum import Enum
from math import inf
from sgi.transform import Vector
from sgi.object import Window
from sgi.displayfile import DisplayFile
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk

class Intersection(Enum):
    # Tipos de interseção.
    NULL = 1
    LEFT = 2
    RIGHT = 3
    TOP = 4
    BOTTOM = 5


class Viewport():
    _main_window: None
    _drawing_area: Gtk.DrawingArea
    _bg_color: tuple
    _window: Window
    _drag_coord: Vector
    _viewport_padding: Vector

    def __init__(self,
                 main_window: DisplayFile,
                 drawing_area: Gtk.DrawingArea,
                 viewport_padding: Vector = Vector(0.0, 0.0, 0.0),
                 bg_color: tuple = (0, 0, 0)):

        self._main_window = main_window
        self._drawing_area = drawing_area
        self._drawing_area.connect("draw", self.on_draw)
        self._drawing_area.set_events(Gdk.EventMask.ALL_EVENTS_MASK)
        self._drawing_area.connect("button-press-event", self.on_button_press)
        self._drawing_area.connect("motion-notify-event", self.on_mouse_motion)
        self._drawing_area.connect("button-release-event", self.on_button_release)
        self._drawing_area.connect("scroll-event", self.on_scroll)
        self._drawing_area.connect("size-allocate", self.on_size_allocate)
        self._bg_color = bg_color
        self._window = Window(Vector(-500.0, -500.0), Vector(500.0, 500.0), (1.0, 0.0, 0.0), 2.0)
        self._drag_coord = None
        self._viewport_padding = viewport_padding

    def world_to_screen(self, coord: Vector):
        # Converte a coordenada de mundo para uma coordenada de tela.
        origin = self._window.normalized_origin - self._viewport_padding
        extension = self._window.normalized_extension + self._viewport_padding

        x_s = ((coord.x - origin.x) / (extension.x - origin.x)) * (self._drawing_area.get_allocated_width())
        y_s = (1 - (coord.y - origin.y) / (extension.y - origin.y)) * self._drawing_area.get_allocated_height()

        return Vector(x_s, y_s)

    def world_line_to_screen(self, line: list[Vector]):
        # Converte uma linha no mundo para uma linha na tela.
        return (self.world_to_screen(line[0]), self.world_to_screen(line[1]))

    def screen_to_world(self, coord: Vector):
        # Converte a coordenada de tela para uma coordenada de mundo.
        origin = self._window.origin - self._viewport_padding
        extension = self._window.extension + self._viewport_padding

        x_w = (coord.x / self._drawing_area.get_allocated_width()) * (extension.x - origin.x) + origin.x
        y_w = (1.0 - (coord.y / self._drawing_area.get_allocated_height())) * (extension.y - origin.y) + origin.y

        return Vector(x_w, y_w)

    def clip_to_lines(self, coords: list[Vector]):
        # O algoritmo de clipping de polígonos é o Sutherland-Hodgeman.
        clipped_lines = []
        coords_size = len(coords)
        if coords_size == 2:
            clipped_line = self.cohen_sutherland(coords)
            if len(clipped_line) > 0:
                clipped_lines.append(clipped_line)

        else:
            clipped_lines = self.coords_to_lines(coords)
            clipped_coords = []

            for inter in [Intersection.LEFT, Intersection.RIGHT, Intersection.BOTTOM, Intersection.TOP]:
                for line in clipped_lines:
                    comp_inside = None
                    comp_a = None
                    comp_b = None

                    match inter:
                        case Intersection.LEFT:
                            comp_inside = line[0].x > self._window.normalized_origin.x and \
                                          line[1].x > self._window.normalized_origin.x
                            comp_a = line[0].x > self._window.normalized_origin.x
                            comp_b = line[1].x > self._window.normalized_origin.x
                        case Intersection.RIGHT:
                            comp_inside = line[0].x < self._window.normalized_extension.x and \
                                          line[1].x < self._window.normalized_extension.x
                            comp_a = line[0].x < self._window.normalized_extension.x
                            comp_b = line[1].x < self._window.normalized_extension.x
                        case Intersection.BOTTOM:
                            comp_inside = line[0].y > self._window.normalized_origin.y and \
                                          line[1].y > self._window.normalized_origin.y
                            comp_a = line[0].y > self._window.normalized_origin.y
                            comp_b = line[1].y > self._window.normalized_origin.y
                        case Intersection.TOP:
                            comp_inside = line[0].y < self._window.normalized_extension.y and \
                                          line[1].y < self._window.normalized_extension.y
                            comp_a = line[0].y < self._window.normalized_extension.y
                            comp_b = line[1].y < self._window.normalized_extension.y

                    if comp_inside:
                        clipped_coords.append(line[0])
                        clipped_coords.append(line[1])
                    elif comp_a:
                        intersection = self.intersection(line, None, inter, False)
                        clipped_coords.append(intersection[0])
                        clipped_coords.append(intersection[1])
                    elif comp_b:
                        intersection = self.intersection(line, inter, None, False)
                        clipped_coords.append(intersection[0])
                        clipped_coords.append(intersection[1])

                clipped_lines = self.coords_to_lines(clipped_coords)
                clipped_coords.clear()

        return clipped_lines

    def intersection(self,
                     line: list[Vector],
                     inter_a: Intersection,
                     inter_b: Intersection,
                     drop_line: bool = True):
        # Cacula a interseção do vetor com a window.
        angular_coeff = inf

        if (line[1].x - line[0].x) != 0:
            angular_coeff = (line[1].y - line[0].y) / (line[1].x - line[0].x)

        new_line = []

        for inter, vector in zip([inter_a, inter_b], line):

            new_x = vector.x
            new_y = vector.y

            match inter:
                case Intersection.RIGHT:
                    new_x = self._window.normalized_origin.x
                    new_y = angular_coeff * (self._window.normalized_origin.x - vector.x) + vector.y

                    if (new_y < self._window.normalized_origin.y or new_y > self._window.normalized_extension.y) and \
                       drop_line:
                        return []
                case Intersection.LEFT:
                    new_x = self._window.normalized_extension.x
                    new_y = angular_coeff * (self._window.normalized_extension.x - vector.x) + vector.y

                    if (new_y < self._window.normalized_origin.y or new_y > self._window.normalized_extension.y) and \
                       drop_line:
                        return []
                case Intersection.BOTTOM:
                    new_x = vector.x + (1.0 / angular_coeff) * (self._window.normalized_extension.y - vector.y)
                    new_y = self._window.normalized_extension.y

                    if (new_x < self._window.normalized_origin.x or new_x > self._window.normalized_extension.x) and \
                       drop_line:
                        return []
                case Intersection.TOP:
                    new_x = vector.x + (1.0 / angular_coeff) * (self._window.normalized_origin.y - vector.y)
                    new_y = self._window.normalized_origin.y

                    if (new_x < self._window.normalized_origin.x or new_x > self._window.normalized_extension.x) and \
                       drop_line:
                        return []

            new_line.append(Vector(new_x, new_y))

        return new_line

    def cohen_sutherland(self, line: list[Vector]):
        # Clipping de algoritmo de Cohen-Shuterland.
        clipped_line = []
        region_codes = []

        for coord in line:

            region_code = 0b0000
            region_code |= 0b0001 if coord.x < self._window.normalized_origin.x else 0b1000
            region_code |= 0b0010 if coord.x > self._window.normalized_extension.x else 0b0100
            region_code |= 0b0100 if coord.y < self._window.normalized_origin.y else 0b0000
            region_code |= 0b1000 if coord.y > self._window.normalized_extension.y else 0b0001
            region_codes.append(region_code)

        if region_codes[0] | region_codes[1] == 0b0000:
            clipped_line = line
        elif region_codes[0] & region_codes[1] == 0b0000:
            intersections = []

            for region_code in region_codes:
                match region_code:
                    case 0b0000:
                        intersections.append(Intersection.NULL)
                    case 0b0001:
                        intersections.append(Intersection.BOTTOM)
                    case 0b0010:
                        intersections.append(Intersection.RIGHT)
                    case 0b1000:
                        intersections.append(Intersection.LEFT)
                    case 0b0100:
                        intersections.append(Intersection.RIGHT)
                    case _:
                        intersections.append(None)

            if intersections[0] is not None and intersections[1] is not None:
                clipped_line = self.intersection(line, intersections[0], intersections[1])
            else:
                for try_index in [(0, 0), (0, 1), (1, 0), (1, 1)]:
                    clipped_line = self.intersection(line,
                                                     double_try_intersections[0][try_index[0]],
                                                     double_try_intersections[1][try_index[1]])

                    if len(clipped_line) > 0:
                        break

        return clipped_line

    def coords_to_lines(self, coords: list[Vector]):
        # Converte coordenadas normais para linhas.
        lines = []

        if len(coords) == 1:
            lines.append([coords[0], Vector(coords[0].x + 1, coords[0].y)])
        else:
            for i, _ in enumerate(coords):
                if i < len(coords) - 1:
                    lines.append([coords[i], coords[i + 1]])

            if len(coords) > 2:
                lines.append([coords[-1], coords[0]])

        return lines

    # Handlers
    def on_draw(self, area, context):
        # Normaliza os objetos
        self._main_window.display_file.normalize_objects(self._window)

        # Preenche o fundo
        context.set_source_rgb(self._bg_color[0], self._bg_color[1], self._bg_color[2])
        context.rectangle(0, 0, area.get_allocated_width(), area.get_allocated_height())
        context.fill()

        # Renderiza todos os objetos do display file
        for obj in self._main_window.display_file.objects + [self._window]:
            clipped_coords = []

            if obj != self._window:
                clipped_coords = self.clip_to_lines(obj.normalized_coords)
            else:
                clipped_coords = self.coords_to_lines(obj.normalized_coords)

            screen_lines = list(map(self.world_line_to_screen, clipped_coords))
            color = obj.color
            line_width = obj.line_width

            # Define cor e largura do pincel
            context.new_path()
            context.set_source_rgb(color[0], color[1], color[2])
            context.set_line_width(line_width)

            for line in screen_lines:
                if obj.fill:
                    context.line_to(line[1].x, line[1].y)
                else:
                    context.move_to(line[0].x, line[0].y)
                    context.line_to(line[1].x, line[1].y)
                    context.stroke()

            context.close_path()

            if obj.fill:
                context.fill()

        self._drawing_area.queue_draw()

    def on_button_press(self, widget, event):
        # Evento de clique.
        position = Vector(event.x, event.y)

        if event.button == 1:
            self._main_window.editor.click(self.screen_to_world(position))
        elif event.button == 2:
            self._drag_coord = position

    def on_mouse_motion(self, widget, event):
        # Evento de movimento.
        if self._drag_coord is not None:
            position = Vector(event.x, event.y)
            diff = self._drag_coord - position
            diff.y = -diff.y
            diff *= self._window.scale.x
            self.move_window(diff)
            self._drag_coord = position

    def on_button_release(self, widget, event):
        # Evento de liberação do mouse.
        if event.button == 2:
            self._drag_coord = None

    def on_scroll(self, widget, event):
        # Evento de rolagem:
        direction = event.get_scroll_deltas()[2]

        if direction > 0:
            self._window.rescale(Vector(1.03, 1.03, 1.0))
        else:
            self._window.rescale(Vector(0.97, 0.97, 1.0))

        self._main_window.display_file.request_normalization()

    def on_size_allocate(self, allocation, user_data):
        # Evento de alocação.
        self.reset_window_scale()
        self._main_window.display_file.request_normalization()

    def move_window(self, direction: Vector):
        # Move a window.
        self._window.translate(direction, True)
        self._main_window.display_file.request_normalization()

    def reset_window_position(self):
        # Redefine a posição da window.
        self._window.translate(self._window.position * -1)
        self._main_window.display_file.request_normalization()

    def rotate_window(self, angle: float):
        # Rotaciona a window.
        self._window.rotate(angle)
        self._main_window.display_file.request_normalization()

    def reset_window_rotation(self):
        # Redefine a rotação da window.
        self._window.rotate(-self._window.rotation.z)
        self._main_window.display_file.request_normalization()

    def reescale_window(self, scale: Vector):
        # Reescala a window.
        self._window.rescale(scale)
        self._main_window.display_file.request_normalization()

    def reset_window_scale(self):
        # Redefine a escala da window.
        diff_x = 1.0 / self._window.scale.x
        diff_y = 1.0 / self._window.scale.y
        diff_z = 1.0 / self._window.scale.z

        self._window.rescale(Vector(diff_x, diff_y, diff_z))
        self._main_window.display_file.request_normalization()
