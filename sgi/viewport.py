# -*- coding: utf-8 -*-

from sgi.transform import Vector
from sgi.object import Rectangle
from sgi.displayfile import DisplayFile
import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk


class Viewport():
    _main_window: None
    _drawing_area: Gtk.DrawingArea
    _bg_color: tuple
    _window: Rectangle
    _drag_coord: Vector

    def __init__(self,
                 main_window: DisplayFile,
                 drawing_area: Gtk.DrawingArea,
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
        self._window = Rectangle(Vector(0.0, 0.0), Vector(922.0, 623.0), "Window", (0.5, 0.0, 0.5), 1.0)
        self._drag_coord = None

    def coords_to_screen(self, coord: Vector):
        # Converte a coordenada de mundo para uma coordenada de tela.
        origin = self._window.origin
        extension = self._window.extension

        x = ((coord.x - origin.x) / (extension.x - origin.x)) * self._drawing_area.get_allocated_width()
        y = (1 - (coord.y - origin.y) / (extension.y - origin.y)) * self._drawing_area.get_allocated_height()

        return Vector(x, y)

    def screen_to_coords(self, coord: Vector):
        # Converte a coordenada de tela para uma coordenada de mundo.

        origin = self._window.origin
        extension = self._window.extension

        x = (coord.x / self._drawing_area.get_allocated_width()) * (extension.x - origin.x) + origin.x
        y = (1.0 - (coord.y / self._drawing_area.get_allocated_height())) * (extension.y - origin.y) + origin.y

        return Vector(x, y)

    def coords_to_lines(self, coords: list[Vector]):
        # Converte coordenadas normais para linhas.
        lines = []

        if len(coords) == 1:
            lines.append((coords[0], Vector(coords[0].x + 1, coords[0].y)))
        else:
            for i, _ in enumerate(coords):
                if i < len(coords) - 1:
                    lines.append((coords[i], coords[i + 1]))

            if (len(coords) // 3) % 2 != 0:
                lines.append((coords[-1], coords[0]))

        return lines

    # Handlers
    def on_draw(self, area, context):
        # Background
        context.set_source_rgb(self._bg_color[0], self._bg_color[1], self._bg_color[2])
        context.rectangle(0, 0, area.get_allocated_width(), area.get_allocated_height())
        context.fill()

        # Renderiza todos os objetos do display file
        for obj in self._main_window.display_file.objects + [self._window]:
            screen_coords = list(map(self.coords_to_screen, obj.coord_list))
            lines = self.coords_to_lines(screen_coords)
            color = obj.color
            line_width = obj.line_width

            # Define cor e largura
            context.set_source_rgb(color[0], color[1], color[2])
            context.set_line_width(line_width)

            for line in lines:
                context.move_to(line[0].x, line[0].y)
                context.line_to(line[1].x, line[1].y)
                context.stroke()

        self._drawing_area.queue_draw()

    def on_button_press(self, widget, event):
        # Evento de clique.
        position = Vector(event.x, event.y)

        if event.button == 1:
            self._main_window.editor.click(self.screen_to_coords(position))
        elif event.button == 2:
            self._drag_coord = position

    def on_mouse_motion(self, widget, event):
        # Movimento do mouse.
        if self._drag_coord is not None:
            position = Vector(event.x, event.y)
            diff = self._drag_coord - position
            diff.y = -diff.y
            diff *= self._window.scale.x
            self._window.translate(diff)
            self._drag_coord = position

    def on_button_release(self, widget, event):
        # Evento de liberação do mouse.
        if event.button == 2:
            self._drag_coord = None

    def on_scroll(self, widget, event):
        # Evento de scroll
        direction = event.get_scroll_deltas()[2]

        if direction > 0:
            self._window.rescale(Vector(1.03, 1.03, 1.0))
        else:
            self._window.rescale(Vector(0.97, 0.97, 1.0))

    def on_size_allocate(self, allocation, user_data):
        diff = Vector(1.0, 1.0, 1.0)

        diff.x /= self._window.scale.x
        diff.y /= self._window.scale.y
        diff.z /= self._window.scale.z

        self._window.rescale(diff)
        self._window.rescale(Vector(user_data.width / self._window.extension.x,
                                    user_data.height / self._window.extension.y,
                                    1.0))